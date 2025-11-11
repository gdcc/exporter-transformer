import urllib2
import json

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
        content = response.read()
        # Try to parse as JSON to validate
        parsed = json.loads(content)
        return parsed
    except:
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
    
    # Find CDI files (application/ld+json with DDI-CDI profile MIME type)
    cdi_files = []
    for file_info in files:
        datafile = file_info.get('dataFile', {})
        content_type = datafile.get('contentType', '')
        
        # Check for application/ld+json with DDI-CDI profile
        # Accept both the full profile and just application/ld+json for now (transition period)
        is_cdi_mime = (
            'ddialliance.org/Specification/DDI-CDI' in content_type or
            (content_type == 'application/ld+json' and datafile.get('filename', '').endswith('.jsonld'))
        )
        
        if is_cdi_mime:
            # Check if it has .jsonld extension
            filename = datafile.get('filename', '')
            if filename.endswith('.jsonld'):
                cdi_files.append({
                    'id': datafile.get('id'),
                    'filename': filename,
                    'createDate': datafile.get('createDate', '')
                })
    
    # Sort by creation date (newest first) and get the most recent
    if cdi_files:
        cdi_files.sort(key=lambda f: f.get('createDate', ''), reverse=True)
        latest_file = cdi_files[0]
        
        # Download and return the content
        content = get_cdi_file_content(site_url, latest_file['id'])
        if content:
            return content
    
    return None

# Try to get existing CDI file first
existing_cdi = find_cdi_file()
if existing_cdi:
    res = existing_cdi
else:
    # Generate CDI JSON-LD from dataset metadata
    res = {}
    
    # Set up JSON-LD context
    context = {}
    context['@vocab'] = 'https://ddialliance.org/Specification/DDI-CDI/1.0/RDF/'
    context['ddi'] = 'https://ddialliance.org/Specification/DDI-CDI/1.0/RDF/'
    context['xsd'] = 'http://www.w3.org/2001/XMLSchema#'
    context['rdf'] = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    context['rdfs'] = 'http://www.w3.org/2000/01/rdf-schema#'
    context['skos'] = 'http://www.w3.org/2004/02/skos/core#'
    res['@context'] = context
    
    # Use @graph for flattened JSON-LD structure
    graph = []
    
    # Get basic dataset information
    dataset_json = x.get('datasetJson', {})
    schema_org = x.get('datasetSchemaDotOrg', {})
    ore_data = x.get('datasetORE', {})
    
    # Create Dataset Description
    dataset_description = {}
    dataset_description['@type'] = 'DatasetDescription'
    
    # Generate dataset ID
    dataset_id = dataset_json.get('identifier')
    if dataset_id:
        dataset_description['@id'] = 'dataset-' + str(dataset_id)
    else:
        dataset_description['@id'] = 'dataset-1'
    
    # Add title
    if 'name' in schema_org:
        dataset_description['name'] = schema_org['name']
    elif 'datasetVersion' in dataset_json:
        metadata = dataset_json['datasetVersion'].get('metadataBlocks', {})
        if 'citation' in metadata and 'fields' in metadata['citation']:
            for field in metadata['citation']['fields']:
                if field.get('typeName') == 'title':
                    dataset_description['name'] = field.get('value', '')
                    break
    
    # Add description
    if 'description' in schema_org:
        if isinstance(schema_org['description'], list) and len(schema_org['description']) > 0:
            dataset_description['description'] = schema_org['description'][0]
        elif isinstance(schema_org['description'], str):
            dataset_description['description'] = schema_org['description']
    
    # Add identifier (DOI/Handle)
    if 'identifier' in schema_org:
        dataset_description['identifier'] = schema_org['identifier']
    elif 'ore:describes' in ore_data:
        describes = ore_data['ore:describes']
        if '@id' in describes:
            dataset_description['identifier'] = describes['@id']
    
    # Add publication date
    if 'datePublished' in schema_org:
        dataset_description['datePublished'] = schema_org['datePublished']
    
    # Add creators/authors
    creators = []
    if 'creator' in schema_org:
        for creator_obj in schema_org['creator']:
            creator = {}
            creator['@type'] = 'Individual'
            if 'name' in creator_obj:
                creator['name'] = creator_obj['name']
            if '@id' in creator_obj:
                creator['@id'] = creator_obj['@id']
            elif 'name' in creator_obj:
                # Generate ID from name
                creator['@id'] = 'creator-' + creator_obj['name'].replace(' ', '-').lower()
            
            # Add affiliation if available
            if 'affiliation' in creator_obj:
                affiliation = {}
                affiliation['@type'] = 'Organization'
                if isinstance(creator_obj['affiliation'], dict):
                    affiliation['name'] = creator_obj['affiliation'].get('name', '')
                else:
                    affiliation['name'] = creator_obj['affiliation']
                creator['affiliation'] = affiliation
            
            creators.append(creator)
    
    if creators:
        dataset_description['creators'] = creators
    
    # Add keywords/subjects
    if 'keywords' in schema_org and schema_org['keywords']:
        dataset_description['keywords'] = schema_org['keywords']
    
    # Add license
    if 'license' in schema_org:
        license_info = schema_org['license']
        if isinstance(license_info, dict):
            dataset_description['license'] = license_info.get('url') or license_info.get('@id') or license_info.get('name')
        else:
            dataset_description['license'] = license_info
    
    # Add publisher
    if 'publisher' in schema_org:
        publisher = {}
        publisher['@type'] = 'Organization'
        if isinstance(schema_org['publisher'], dict):
            publisher['name'] = schema_org['publisher'].get('name', '')
            if 'url' in schema_org['publisher']:
                publisher['url'] = schema_org['publisher']['url']
        else:
            publisher['name'] = schema_org['publisher']
        dataset_description['publisher'] = publisher
    
    graph.append(dataset_description)
    
    # Process data files and create DataStore entries
    file_details = x.get('datasetFileDetails', [])
    if file_details:
        for idx, file_info in enumerate(file_details):
            # Create DataStore for each file
            datastore = {}
            datastore['@type'] = 'DataStore'
            datastore['@id'] = 'datastore-' + str(idx + 1)
            
            # Get filename
            filename = file_info.get('originalFileName') or file_info.get('filename', '')
            datastore['name'] = filename
            
            # Add description if available
            if 'description' in file_info:
                datastore['description'] = file_info['description']
            
            # Add file format
            file_format = file_info.get('originalFileFormat') or file_info.get('contentType', '')
            if file_format:
                datastore['format'] = file_format
            
            # Add file size
            file_size = file_info.get('originalFileSize') or file_info.get('filesize')
            if file_size:
                datastore['size'] = str(file_size)
            
            # Add checksum
            if 'checksum' in file_info:
                checksum = file_info['checksum']
                datastore['checksum'] = {
                    'algorithm': checksum.get('type', ''),
                    'value': checksum.get('value', '')
                }
            
            graph.append(datastore)
            
            # Process variables if available
            data_tables = file_info.get('dataTables', [])
            for table_idx, data_table in enumerate(data_tables):
                data_variables = data_table.get('dataVariables', [])
                
                for var_idx, var_info in enumerate(data_variables):
                    # Create Variable
                    variable = {}
                    variable['@type'] = 'Variable'
                    variable['@id'] = 'variable-' + str(var_info.get('id', str(idx) + '-' + str(var_idx)))
                    variable['name'] = var_info.get('name', '')
                    
                    # Add label (description)
                    if 'label' in var_info:
                        variable['label'] = var_info['label']
                    
                    # Add variable type information
                    var_format = var_info.get('variableFormatType', '')
                    var_interval = var_info.get('variableIntervalType', '')
                    
                    if var_format == 'CHARACTER':
                        variable['dataType'] = 'string'
                    elif var_format == 'NUMERIC':
                        if var_interval == 'discrete':
                            variable['dataType'] = 'integer'
                        elif var_interval == 'contin':
                            variable['dataType'] = 'float'
                        else:
                            variable['dataType'] = 'numeric'
                    
                    # Add measurement unit if available
                    if 'unf' in var_info:
                        variable['fingerprint'] = var_info['unf']
                    
                    # Link to datastore
                    variable['sourceDataStore'] = {'@id': 'datastore-' + str(idx + 1)}
                    
                    graph.append(variable)
    
    # Add DataSet entry that ties everything together
    dataset = {}
    dataset['@type'] = 'DataSet'
    dataset['@id'] = 'dataset'
    dataset['describes'] = {'@id': dataset_description['@id']}
    
    # Link to data stores
    datastore_refs = [{'@id': item['@id']} for item in graph if item.get('@type') == 'DataStore']
    if datastore_refs:
        dataset['hasDataStores'] = datastore_refs
    
    graph.append(dataset)
    
    # Set the graph
    res['@graph'] = graph
