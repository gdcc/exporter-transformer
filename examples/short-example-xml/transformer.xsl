<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <dataset>
      <title>
        <xsl:value-of select="root/datasetVersion/metadataBlocks/citation/title" />
      </title>
      <xsl:for-each select="root/datasetVersion/metadataBlocks/citation/author">
        <author>
          <xsl:for-each select="authorName">
            <authorName>
              <xsl:value-of select="authorName" />
            </authorName>
          </xsl:for-each>
        </author>
      </xsl:for-each>
      <xsl:for-each select="root/datasetVersion/files">
        <file>
          <xsl:value-of select="dataFile/filename" />
        </file>
      </xsl:for-each>
    </dataset>
  </xsl:template>
</xsl:stylesheet>