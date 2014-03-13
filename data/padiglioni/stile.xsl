<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:a="http://www.imperofiere.com"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform" exclude-result-prefixes="a">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
<xsl:template match="/">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it"> 
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <head>
    <title>Prova</title>
  </head>
  <body>
  <h2>Ciao mondo</h2> 
  <xsl:for-each select="a:padiglioni/a:padiglione">
  <xsl:value-of select="@id"/> <br /> 


  </xsl:for-each>
  </body> 


</html>
</xsl:template>
</xsl:stylesheet>
