import urllib2
import json
import re

# Function to fetch file list from dataset
def get_dataset_files(site_url, dataset_id):
    """Fetch the list of files in the dataset version"""
    try:
        url = site_url + '/api/datasets/' + str(dataset_id) + '/versions/:latest'
        request = urllib2.Request(url)
        request.add_header('Accept', 'application/json')
        response = urllib2.urlopen(request, timeout=30)
        data = json.loads(response.read())
        
        if data.get('status') == 'OK' and 'data' in data:
            return data['data'].get('files', [])
        return []
    except:
        return []

# Function to download CDI file content
def get_cdi_file_content(site_url, file_id):
    """Download the content of a CDI file"""
    try:
        url = site_url + '/api/access/datafile/' + str(file_id)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request, timeout=30)
        return response.read()
    except Exception as e:
        import sys
        sys.stderr.write('Error downloading CDI file: ' + str(e) + '\n')
        return None

# Try to find and return existing CDI file
def find_cdi_file():
    """Find the latest CDI file with application/ld+json MIME type"""
    
    # Extract site URL and dataset ID from the input data
    site_url = None
    dataset_id = None
    
    # Try to get site URL from ORE export
    if 'datasetORE' in x and 'ore:describes' in x['datasetORE']:
        describes = x['datasetORE']['ore:describes']
        if '@id' in describes:
            dataset_url = describes['@id']
            # Extract base URL (everything before /dataset.xhtml or /api)
            if '/dataset.xhtml' in dataset_url:
                site_url = dataset_url.split('/dataset.xhtml')[0]
            elif '/citation' in dataset_url:
                site_url = dataset_url.split('/citation')[0]
    
    # Try to get dataset ID from datasetJson
    if 'datasetJson' in x and 'id' in x['datasetJson']:
        dataset_id = x['datasetJson']['id']
    
    if not site_url or not dataset_id:
        return None
    
    # Get list of files
    files = get_dataset_files(site_url, dataset_id)
    
    # Find CDI files - ONLY files with exact DDI-CDI MIME type
    cdi_files = []
    try:
        for file_info in files:
            try:
                # Safe access for Jython/Java HashMap
                datafile = None
                try:
                    datafile = file_info.get('dataFile')
                except:
                    try:
                        datafile = file_info['dataFile']
                    except:
                        continue
                
                if not datafile:
                    continue
                
                # Get content type safely
                content_type = ''
                try:
                    content_type = datafile.get('contentType', '')
                except:
                    try:
                        content_type = datafile['contentType']
                    except:
                        content_type = ''
                
                if not content_type:
                    continue
                
                # Check for EXACT MIME type: application/ld+json with DDI-CDI profile
                # Must match: application/ld+json with ddialliance.org profile (case-insensitive)
                content_type_str = str(content_type).lower()
                is_cdi_mime = (
                    'application/ld+json' in content_type_str and 
                    'profile=' in content_type_str and
                    'ddialliance.org' in content_type_str and
                    'ddi-cdi' in content_type_str
                )
                
                if is_cdi_mime:
                    # Safely extract file metadata
                    file_id = None
                    filename = ''
                    create_date = ''
                    
                    try:
                        file_id = datafile.get('id')
                    except:
                        try:
                            file_id = datafile['id']
                        except:
                            pass
                    
                    try:
                        filename = datafile.get('filename', '')
                    except:
                        try:
                            filename = datafile['filename']
                        except:
                            pass
                    
                    try:
                        create_date = datafile.get('createDate', '')
                    except:
                        try:
                            create_date = datafile['createDate']
                        except:
                            pass
                    
                    if file_id:
                        cdi_files.append({
                            'id': file_id,
                            'filename': filename,
                            'createDate': create_date
                        })
            except:
                pass
    except:
        pass
    
    # Sort by creation date (newest first) and get the most recent
    if cdi_files:
        cdi_files.sort(key=lambda f: f.get('createDate', ''), reverse=True)
        latest_file = cdi_files[0]
        
        # Download and return the content
        content = get_cdi_file_content(site_url, latest_file['id'])
        if content:
            return content
    
    return None

# Helper functions
def sanitize_id(text):
    """Convert text to a valid ID"""
    if not text:
        return 'unknown'
    sanitized = re.sub(r'[^a-zA-Z0-9-_]', '-', str(text))
    sanitized = re.sub(r'-+', '-', sanitized).strip('-').lower()
    return sanitized if sanitized else 'unknown'

def get_field_value(fields, field_name):
    """Extract value from metadata fields array"""
    if not fields:
        return None
    for field in fields:
        if field.get('typeName') == field_name:
            return field.get('value')
    return None

def get_compound_values(fields, field_name):
    """Extract compound field values"""
    if not fields:
        return []
    for field in fields:
        if field.get('typeName') == field_name:
            value = field.get('value', [])
            if isinstance(value, list):
                return value
            elif value:
                return [value]
    return []

# Try to get existing CDI file first
existing_cdi = find_cdi_file()
if existing_cdi:
    res = existing_cdi
else:
    # Generate CDI JSON-LD from dataset metadata
    res = {}
    
    # Set up JSON-LD context
    context = {
        '@vocab': 'http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/',
        'ddi': 'http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/',
        'xsd': 'http://www.w3.org/2001/XMLSchema#',
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
        'skos': 'http://www.w3.org/2004/02/skos/core#'
    }
    res['@context'] = context
    
    # Use @graph for flattened JSON-LD structure
    graph = []
    
    # Get basic dataset information
    dataset_json = x.get('datasetJson', {})
    schema_org = x.get('datasetSchemaDotOrg', {})
    ore_data = x.get('datasetORE', {})
    
    # Get metadata blocks for detailed mapping
    metadata_blocks = {}
    if 'datasetVersion' in dataset_json:
        metadata_blocks = dataset_json['datasetVersion'].get('metadataBlocks', {})
    
    # Extract citation fields
    citation_fields = []
    citation_data_direct = {}
    if 'citation' in metadata_blocks:
        citation_data = metadata_blocks['citation']
        if 'fields' in citation_data:
            citation_fields = citation_data['fields']
        else:
            # Handle pre-transformed format
            citation_data_direct = citation_data
    
    # Helper to get from citation block
    def get_citation_value(field_name):
        # Try from fields array first
        val = get_field_value(citation_fields, field_name)
        if val is not None:
            return val
        # Try from direct properties
        return citation_data_direct.get(field_name)
    
    def get_citation_compound(field_name):
        # Try from fields array first
        vals = get_compound_values(citation_fields, field_name)
        if vals:
            return vals
        # Try from direct properties
        direct_val = citation_data_direct.get(field_name)
        if isinstance(direct_val, list):
            return direct_val
        elif direct_val:
            return [direct_val]
        return []
    
    # Create main Dataset ID
    dataset_id = dataset_json.get('identifier')
    if not dataset_id:
        dataset_id = 'dataset-1'
    else:
        dataset_id = sanitize_id(dataset_id)
    
    dataset_persistent_id = dataset_json.get('persistentUrl') or schema_org.get('identifier') or dataset_json.get('identifier', '')
    
    # Create primary DataSet (maps to cdi:DataSet)
    main_dataset = {
        '@type': 'DataSet',
        '@id': '#DataSet_' + dataset_id
    }
    
    # Add name (title)
    title = schema_org.get('name') or get_citation_value('title') or 'Untitled Dataset'
    main_dataset['name'] = [{'@language': 'en', '@value': title}]
    
    # Add subtitle if available
    subtitle = get_citation_value('subtitle')
    if subtitle:
        main_dataset['name'].append({'@language': 'en', '@value': subtitle})
    
    # Add alternative titles
    alt_titles = get_citation_compound('alternativeTitle')
    for alt_title in alt_titles:
        if alt_title:
            main_dataset['name'].append({'@language': 'en', '@value': alt_title})
    
    # Add identifier
    if dataset_persistent_id:
        main_dataset['identifier'] = {'@type': 'Identifier', 'identifier': dataset_persistent_id}
    
    # Add description (purpose in CDI terms)
    description = None
    if 'description' in schema_org:
        if isinstance(schema_org['description'], list) and len(schema_org['description']) > 0:
            description = schema_org['description'][0]
        elif isinstance(schema_org['description'], str):
            description = schema_org['description']
    
    # Also check dsDescription from citation
    ds_desc_list = get_citation_compound('dsDescription')
    if ds_desc_list:
        for desc_obj in ds_desc_list:
            if isinstance(desc_obj, dict) and 'dsDescriptionValue' in desc_obj:
                description = desc_obj['dsDescriptionValue']
                break
            elif isinstance(desc_obj, basestring):
                description = desc_obj
                break
    
    if description:
        main_dataset['purpose'] = {'@language': 'en', '@value': description}
    
    # Add catalog details
    catalog_details = {}
    if 'publisher' in dataset_json:
        catalog_details['identifier'] = dataset_json['publisher']
    
    depositor = get_citation_value('depositor')
    if depositor:
        catalog_details['depositor'] = depositor
    
    if catalog_details:
        main_dataset['catalogDetails'] = catalog_details
    
    graph.append(main_dataset)
    
    # Create Agents (Individuals and Organizations)
    agent_refs = []
    
    # Process authors/creators
    authors = get_citation_compound('author') or schema_org.get('creator', [])
    if authors:
        try:
            for idx, author_obj in enumerate(authors):
                try:
                    author_name = ''
                    try:
                        author_name = author_obj.get('authorName') or author_obj.get('name', '')
                    except:
                        author_name = str(author_obj) if author_obj else ''
                    
                    if not author_name:
                        continue
                    
                    agent_id = '#Agent_Author_' + sanitize_id(author_name)
                    agent = {
                        '@type': 'Individual',
                        '@id': agent_id,
                        'identifier': {'@type': 'Identifier', 'identifier': author_name}
                    }
                    
                    # Add ORCID if available
                    try:
                        orcid = author_obj.get('authorIdentifier')
                        if orcid:
                            agent['identifier'] = {
                                '@type': 'Identifier',
                                'identifier': orcid
                            }
                    except:
                        pass
                    
                    # Add affiliation
                    try:
                        affiliation_name = author_obj.get('authorAffiliation')
                        if not affiliation_name:
                            try:
                                affiliation_obj = author_obj.get('affiliation')
                                try:
                                    affiliation_name = affiliation_obj.get('name')
                                except:
                                    affiliation_name = str(affiliation_obj) if affiliation_obj else None
                            except:
                                pass
                        
                        if affiliation_name:
                            org_id = '#Agent_Org_' + sanitize_id(affiliation_name)
                            org = {
                                '@type': 'Organization',
                                '@id': org_id,
                                'identifier': {'@type': 'Identifier', 'identifier': affiliation_name}
                            }
                            graph.append(org)
                    except:
                        pass
                    
                    graph.append(agent)
                    agent_refs.append({'@id': agent_id})
                except:
                    pass
        except:
            pass
    
    # Process contributors
    contributors = get_citation_compound('contributor')
    if contributors:
        try:
            for contrib_obj in contributors:
                try:
                    contrib_name = ''
                    contrib_type = ''
                    try:
                        contrib_name = contrib_obj.get('contributorName', '')
                        contrib_type = contrib_obj.get('contributorType', '')
                    except:
                        contrib_name = str(contrib_obj) if contrib_obj else ''
                    
                    if not contrib_name:
                        continue
                    
                    agent_id = '#Agent_Contributor_' + sanitize_id(contrib_name)
                    agent = {
                        '@type': 'Individual',
                        '@id': agent_id,
                        'identifier': {'@type': 'Identifier', 'identifier': contrib_name}
                    }
                    
                    if contrib_type:
                        agent['purpose'] = {'@language': 'en', '@value': contrib_type}
                    
                    graph.append(agent)
                    agent_refs.append({'@id': agent_id})
                except:
                    pass
        except:
            pass
    
    # Process producers
    producers = get_citation_compound('producer')
    if producers:
        try:
            for prod_obj in producers:
                try:
                    prod_name = ''
                    try:
                        prod_name = prod_obj.get('producerName', '')
                    except:
                        prod_name = str(prod_obj) if prod_obj else ''
                    
                    if not prod_name:
                        continue
                    
                    agent_id = '#Agent_Producer_' + sanitize_id(prod_name)
                    agent = {
                        '@type': 'Organization',
                        '@id': agent_id,
                        'identifier': {'@type': 'Identifier', 'identifier': prod_name}
                    }
                    
                    try:
                        producer_url = prod_obj.get('producerURL')
                        if producer_url:
                            agent['image'] = [{'@type': 'Image', 'uri': producer_url}]
                    except:
                        pass
                    
                    graph.append(agent)
                    agent_refs.append({'@id': agent_id})
                except:
                    pass
        except:
            pass
    
    # Create AgentListing if we have agents
    if agent_refs:
        agent_listing = {
            '@type': 'AgentListing',
            '@id': '#AgentListing_' + dataset_id,
            'allowsDuplicates': False,
            'purpose': {'@language': 'en', '@value': 'Dataset contributors and creators'}
        }
        graph.append(agent_listing)
    
    # Create InstanceVariable for each variable in tabular data
    file_details = x.get('datasetFileDetails', [])
    variable_refs = []
    
    if file_details:
        try:
            for file_idx, file_info in enumerate(file_details):
                try:
                    try:
                        if not file_info.get('tabularData'):
                            continue
                    except:
                        continue
                    
                    data_tables = file_info.get('dataTables', [])
                    if not data_tables:
                        continue
                    
                    for table_idx, data_table in enumerate(data_tables):
                        try:
                            data_variables = data_table.get('dataVariables', [])
                            if not data_variables:
                                continue
                            
                            for var_info in data_variables:
                                try:
                                    var_id = None
                                    var_name = ''
                                    try:
                                        var_id = var_info.get('id')
                                        var_name = var_info.get('name', '')
                                    except:
                                        continue
                                    
                                    if not var_name:
                                        continue
                                    
                                    instance_var = {
                                        '@type': 'InstanceVariable',
                                        '@id': '#InstanceVariable_' + str(var_id or sanitize_id(var_name)),
                                        'name': [{'@language': 'en', '@value': var_name}]
                                    }
                                    
                                    # Add label (description)
                                    try:
                                        if var_info.get('label'):
                                            instance_var['description'] = {'@language': 'en', '@value': str(var_info['label'])}
                                    except:
                                        pass
                                    
                                    # Add data type
                                    try:
                                        var_format = var_info.get('variableFormatType', '')
                                        var_interval = var_info.get('variableIntervalType', '')
                                        
                                        if var_format == 'CHARACTER':
                                            instance_var['dataType'] = 'string'
                                        elif var_format == 'NUMERIC':
                                            if var_interval == 'discrete':
                                                instance_var['dataType'] = 'integer'
                                            elif var_interval == 'contin':
                                                instance_var['dataType'] = 'decimal'
                                            else:
                                                instance_var['dataType'] = 'numeric'
                                    except:
                                        pass
                                    
                                    # Add format category (date, etc.)
                                    try:
                                        if var_info.get('formatCategory'):
                                            instance_var['formatPattern'] = var_info.get('format', var_info['formatCategory'])
                                    except:
                                        pass
                                    
                                    # Add UNF (Universal Numeric Fingerprint)
                                    try:
                                        if var_info.get('UNF'):
                                            instance_var['identifier'] = {
                                                '@type': 'Identifier',
                                                'identifier': var_info['UNF']
                                            }
                                    except:
                                        pass
                                    
                                    # Add summary statistics if available
                                    try:
                                        stats = var_info.get('summaryStatistics', {})
                                        if stats:
                                            stats_desc = []
                                            try:
                                                if stats.get('min') is not None:
                                                    stats_desc.append('Min: ' + str(stats['min']))
                                            except:
                                                pass
                                            try:
                                                if stats.get('max') is not None:
                                                    stats_desc.append('Max: ' + str(stats['max']))
                                            except:
                                                pass
                                            try:
                                                if stats.get('mean') is not None:
                                                    stats_desc.append('Mean: ' + str(stats['mean']))
                                            except:
                                                pass
                                            try:
                                                if stats.get('medn') is not None:
                                                    stats_desc.append('Median: ' + str(stats['medn']))
                                            except:
                                                pass
                                            try:
                                                if stats.get('stdev') is not None:
                                                    stats_desc.append('StdDev: ' + str(stats['stdev']))
                                            except:
                                                pass
                                            try:
                                                if stats.get('vald') is not None:
                                                    stats_desc.append('Valid: ' + str(stats['vald']))
                                            except:
                                                pass
                                            try:
                                                if stats.get('invd') is not None:
                                                    stats_desc.append('Invalid: ' + str(stats['invd']))
                                            except:
                                                pass
                                            
                                            if stats_desc:
                                                try:
                                                    if 'description' in instance_var:
                                                        current_desc = instance_var['description']['@value']
                                                        instance_var['description']['@value'] = current_desc + ' [' + ', '.join(stats_desc) + ']'
                                                    else:
                                                        instance_var['description'] = {
                                                            '@language': 'en',
                                                            '@value': ', '.join(stats_desc)
                                                        }
                                                except:
                                                    pass
                                    except:
                                        pass
                                    
                                    # Add weighted flag if true
                                    try:
                                        if var_info.get('weighted'):
                                            instance_var['purpose'] = {'@language': 'en', '@value': 'Weighted variable'}
                                    except:
                                        pass
                                    
                                    graph.append(instance_var)
                                    variable_refs.append({'@id': instance_var['@id']})
                                except:
                                    pass
                        except:
                            pass
                except:
                    pass
        except:
            pass
    
    # Create Category objects from categorical variables
    if file_details:
        try:
            for file_info in file_details:
                try:
                    try:
                        if not file_info.get('tabularData'):
                            continue
                    except:
                        continue
                    
                    data_tables = file_info.get('dataTables', [])
                    if not data_tables:
                        continue
                    
                    for data_table in data_tables:
                        try:
                            data_variables = data_table.get('dataVariables', [])
                            if not data_variables:
                                continue
                            
                            for var_info in data_variables:
                                try:
                                    try:
                                        if var_info.get('isOrderedCategorical'):
                                            # This could be expanded with actual category values if available
                                            pass
                                    except:
                                        pass
                                except:
                                    pass
                        except:
                            pass
                except:
                    pass
        except:
            pass
    
    # Add temporal coverage
    time_periods = get_citation_compound('timePeriodCovered')
    if time_periods:
        try:
            for period_obj in time_periods:
                try:
                    start_date = period_obj.get('timePeriodCoveredStart')
                    end_date = period_obj.get('timePeriodCoveredEnd')
                    
                    if start_date or end_date:
                        temporal_coverage = {
                            '@type': 'TemporalCoverage',
                            '@id': '#TemporalCoverage_' + dataset_id
                        }
                        if start_date:
                            temporal_coverage['startDate'] = str(start_date)
                        if end_date:
                            temporal_coverage['endDate'] = str(end_date)
                        
                        graph.append(temporal_coverage)
                except:
                    pass
        except:
            pass
    
    # Add subjects (controlled vocabulary)
    subjects = get_citation_value('subject')
    if subjects:
        try:
            for subject in subjects:
                try:
                    if subject:
                        category = {
                            '@type': 'Category',
                            '@id': '#Subject_' + sanitize_id(str(subject)),
                            'name': [{'@language': 'en', '@value': str(subject)}],
                            'purpose': {'@language': 'en', '@value': 'Subject classification'}
                        }
                        graph.append(category)
                except:
                    pass
        except:
            pass
    
    # Add keywords as Concepts in a CategorySet
    keywords = []
    try:
        keywords = schema_org.get('keywords', [])
    except:
        pass
    keyword_objs = get_citation_compound('keyword')
    
    all_keywords = []
    if keyword_objs:
        try:
            for kw_obj in keyword_objs:
                try:
                    kw_value = ''
                    try:
                        kw_value = kw_obj.get('keywordValue', '')
                    except:
                        kw_value = str(kw_obj) if kw_obj else ''
                    if kw_value:
                        all_keywords.append(str(kw_value))
                except:
                    pass
        except:
            pass
    
    if keywords:
        try:
            for kw in keywords:
                try:
                    if kw and kw not in all_keywords:
                        all_keywords.append(str(kw))
                except:
                    pass
        except:
            pass
    
    if all_keywords:
        try:
            category_set = {
                '@type': 'CategorySet',
                '@id': '#CategorySet_Keywords_' + dataset_id,
                'allowsDuplicates': False,
                'purpose': {'@language': 'en', '@value': 'Dataset keywords and subjects'}
            }
            graph.append(category_set)
            
            for kw in all_keywords[:20]:  # Limit to first 20 keywords
                try:
                    if kw:
                        category = {
                            '@type': 'Category',
                            '@id': '#Category_' + sanitize_id(str(kw)),
                            'name': [{'@language': 'en', '@value': str(kw)}]
                        }
                        graph.append(category)
                except:
                    pass
        except:
            pass
    
    # Add topic classifications
    topic_classifications = get_citation_compound('topicClassification')
    if topic_classifications:
        try:
            for topic_obj in topic_classifications:
                try:
                    topic_value = ''
                    try:
                        topic_value = topic_obj.get('topicClassValue', '')
                    except:
                        pass
                    
                    if topic_value:
                        category = {
                            '@type': 'Category',
                            '@id': '#Topic_' + sanitize_id(str(topic_value)),
                            'name': [{'@language': 'en', '@value': str(topic_value)}],
                            'purpose': {'@language': 'en', '@value': 'Topic classification'}
                        }
                        # Add vocabulary info if available
                        try:
                            vocab = topic_obj.get('topicClassVocab', '')
                            vocab_uri = topic_obj.get('topicClassVocabURI', '')
                            if vocab or vocab_uri:
                                category['description'] = {'@language': 'en', '@value': 'Vocabulary: ' + str(vocab or vocab_uri)}
                        except:
                            pass
                        graph.append(category)
                except:
                    pass
        except:
            pass
    
    # Add languages
    languages = get_citation_value('language')
    if languages:
        try:
            count = 0
            for lang in languages:
                if count >= 5:  # Limit to first 5
                    break
                if lang:
                    # Could create proper language entities, for now add to notes
                    count += 1
        except:
            pass
    
    # Add kind of data
    kind_of_data = get_citation_value('kindOfData')
    if kind_of_data:
        try:
            # Try to join if it's a list/collection
            try:
                kind_of_data = ', '.join(kind_of_data)
            except:
                kind_of_data = str(kind_of_data)
            
            # Add to main dataset purpose or description
            if 'purpose' in main_dataset:
                current_purpose = main_dataset['purpose']['@value']
                main_dataset['purpose']['@value'] = current_purpose + ' | Data type: ' + kind_of_data
            else:
                main_dataset['purpose'] = {'@language': 'en', '@value': 'Data type: ' + kind_of_data}
        except:
            pass
    
    # Add alternative URL
    alt_url = get_citation_value('alternativeURL')
    if alt_url:
        # Could add as proper URL reference
        pass
    
    # Add other IDs
    other_ids = get_citation_compound('otherId')
    if other_ids:
        try:
            for id_obj in other_ids:
                try:
                    agency = ''
                    value = ''
                    try:
                        agency = id_obj.get('otherIdAgency', '')
                        value = id_obj.get('otherIdValue', '')
                    except:
                        pass
                    
                    if agency and value:
                        # Add as additional identifier
                        identifier_obj = {
                            '@type': 'Identifier',
                            '@id': '#Identifier_' + sanitize_id(str(agency) + '_' + str(value)),
                            'identifier': str(agency) + ':' + str(value)
                        }
                        graph.append(identifier_obj)
                except:
                    pass
        except:
            pass
    
    # Add related materials
    related_materials = get_citation_value('relatedMaterial')
    if related_materials:
        try:
            # Try to iterate, if it's a single value it will fail and we skip
            for material in related_materials:
                if material:
                    # Could create proper reference entities
                    pass
        except:
            # Single value, not iterable
            pass
    
    # Add related datasets
    related_datasets = get_citation_value('relatedDatasets')
    if related_datasets:
        if not isinstance(related_datasets, list):
            related_datasets = [related_datasets]
        for dataset_ref in related_datasets:
            if dataset_ref:
                # Could create proper dataset reference entities
                pass
    
    # Add other references
    other_refs = get_citation_value('otherReferences')
    if other_refs:
        if not isinstance(other_refs, list):
            other_refs = [other_refs]
        # Could create reference entities
        pass
    
    # Add data sources information
    data_sources = get_citation_value('dataSources')
    origin_of_sources = get_citation_value('originOfSources')
    characteristics_of_sources = get_citation_value('characteristicOfSources')
    access_to_sources = get_citation_value('accessToSources')
    
    if data_sources or origin_of_sources or characteristics_of_sources or access_to_sources:
        source_desc = []
        if data_sources:
            if isinstance(data_sources, list):
                source_desc.append('Sources: ' + ', '.join(data_sources))
            else:
                source_desc.append('Sources: ' + str(data_sources))
        if origin_of_sources:
            source_desc.append('Origin: ' + str(origin_of_sources))
        if characteristics_of_sources:
            source_desc.append('Characteristics: ' + str(characteristics_of_sources))
        if access_to_sources:
            source_desc.append('Access: ' + str(access_to_sources))
        
        # Create a data source annotation
        if source_desc:
            source_annotation = {
                '@type': 'Annotation',
                '@id': '#DataSourceInfo_' + dataset_id,
                'description': {'@language': 'en', '@value': '; '.join(source_desc)}
            }
            graph.append(source_annotation)
    
    # Add publication/citation information
    publications = get_citation_compound('publication')
    if publications:
        try:
            for pub_obj in publications:
                try:
                    pub_citation = pub_obj.get('publicationCitation', '')
                    if pub_citation:
                        # Could create a fuller structure, for now just note it exists
                        pass
                except:
                    pass
        except:
            pass
    
    # Add grant information
    grants = get_citation_compound('grantNumber')
    if grants:
        try:
            for grant_obj in grants:
                try:
                    agency = grant_obj.get('grantNumberAgency', '')
                    number = grant_obj.get('grantNumberValue', '')
                    if agency or number:
                        # Could create grant/funding structures
                        pass
                except:
                    pass
        except:
            pass
    
    # Add software used
    software_list = get_citation_compound('software')
    if software_list:
        try:
            for sw_obj in software_list:
                try:
                    sw_name = sw_obj.get('softwareName', '')
                    sw_version = sw_obj.get('softwareVersion', '')
                    if sw_name:
                        # Could create software agent
                        pass
                except:
                    pass
        except:
            pass
    
    # Add series information
    series_list = get_citation_compound('series')
    if series_list:
        try:
            for series_obj in series_list:
                try:
                    series_name = series_obj.get('seriesName', '')
                    if series_name:
                        # Could create series/collection structure
                        pass
                except:
                    pass
        except:
            pass
    
    # Add notes
    notes = get_citation_value('notesText')
    if notes:
        # Could add as additional description or annotation
        pass
    
    # Create DataStore entities for files
    files_list = []
    try:
        dataset_version = dataset_json.get('datasetVersion', {})
        files_list = dataset_version.get('files', [])
    except:
        pass
    
    if files_list:
        try:
            for file_entry in files_list:
                try:
                    datafile = file_entry.get('dataFile', {})
                    if not datafile:
                        continue
                    
                    file_id = datafile.get('id')
                    filename = datafile.get('filename', '')
                    
                    if not filename:
                        continue
                    
                    datastore = {
                        '@type': 'DataStore',
                        '@id': '#DataStore_' + str(file_id or sanitize_id(str(filename))),
                        'name': [{'@language': 'en', '@value': str(filename)}]
                    }
                    
                    # Add file size
                    try:
                        filesize = datafile.get('filesize')
                        if filesize:
                            datastore['byteSize'] = str(filesize)
                    except:
                        pass
                    
                    # Add content type
                    try:
                        content_type = datafile.get('contentType', '')
                        if content_type:
                            datastore['format'] = str(content_type)
                    except:
                        pass
                    
                    # Add checksum
                    try:
                        checksum = datafile.get('checksum', {})
                        if checksum:
                            try:
                                checksum_val = checksum.get('value', '') or datafile.get('md5', '')
                                checksum_type = checksum.get('type', 'MD5')
                                if checksum_val:
                                    datastore['identifier'] = {
                                        '@type': 'Identifier',
                                        'identifier': str(checksum_type) + ':' + str(checksum_val)
                                    }
                            except:
                                pass
                    except:
                        pass
                    
                    # Add UNF if available
                    try:
                        unf = datafile.get('UNF')
                        if unf:
                            if 'identifier' not in datastore:
                                datastore['identifier'] = {'@type': 'Identifier', 'identifier': str(unf)}
                    except:
                        pass
                    
                    # Add description with file details
                    try:
                        file_desc = []
                        if datafile.get('tabularData'):
                            file_desc.append('Tabular data file')
                        
                        friendly_type = datafile.get('friendlyType', '')
                        if friendly_type:
                            file_desc.append('Type: ' + str(friendly_type))
                        
                        original_format = datafile.get('originalFormatLabel', '')
                        if original_format:
                            file_desc.append('Original format: ' + str(original_format))
                        
                        if file_desc:
                            datastore['description'] = {'@language': 'en', '@value': ', '.join(file_desc)}
                    except:
                        pass
                    
                    graph.append(datastore)
                except:
                    pass
        except:
            pass
    
    # Add license information
    license_info = dataset_json.get('datasetVersion', {}).get('license', {})
    if license_info:
        license_name = license_info.get('name', '')
        license_uri = license_info.get('uri', '')
        
        if license_name or license_uri:
            # Add to main dataset
            license_obj = {'@language': 'en', '@value': license_name or license_uri}
            if license_uri:
                main_dataset['purpose'] = license_obj
    
    # Add date of collection if not already added
    date_of_collection = get_citation_compound('dateOfCollection')
    if date_of_collection:
        try:
            for period_obj in date_of_collection:
                try:
                    start_date = period_obj.get('dateOfCollectionStart')
                    end_date = period_obj.get('dateOfCollectionEnd')
                    
                    if start_date or end_date:
                        collection_coverage = {
                            '@type': 'TemporalCoverage',
                            '@id': '#CollectionPeriod_' + dataset_id
                        }
                        if start_date:
                            collection_coverage['startDate'] = str(start_date)
                        if end_date:
                            collection_coverage['endDate'] = str(end_date)
                        
                        collection_coverage['purpose'] = {'@language': 'en', '@value': 'Data collection period'}
                        graph.append(collection_coverage)
                except:
                    pass
        except:
            pass
    
    # Add distribution and production dates
    dist_date = dataset_json.get('datasetVersion', {}).get('distributionDate')
    prod_date = dataset_json.get('datasetVersion', {}).get('productionDate')
    
    if dist_date or prod_date:
        date_info = []
        if prod_date:
            date_info.append('Production: ' + prod_date)
        if dist_date:
            date_info.append('Distribution: ' + dist_date)
        
        # Could create proper date entities, for now add to notes
        if date_info:
            pass  # Add to an annotation or note entity if needed
    
        # Set the graph
        res['@graph'] = graph
