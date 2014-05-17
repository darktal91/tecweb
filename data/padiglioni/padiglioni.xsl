<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns="http://www.imperofiere.com" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version='1.0' encoding='UTF-8' indent='yes'/>

  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it"> 
      <head>
	<title>ImperoFiere.it - Padiglioni</title>
	<xsl:call-template name="meta" />
      </head>
      <body>
	<h2>Ciao mondo</h2>
	<xsl:apply-templates select="padiglioni/padiglione"/> 
      </body> 
    </html>
  </xsl:template>

  <xsl:template match="padiglioni/padiglione">
    <xsl:apply-templates select="@id"/>   
  </xsl:template>

  <xsl:template match="@id">
    <xsl:value-of select="."/> <br /> 
  </xsl:template>

  <xsl:template name="meta">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="title" content="Home Page - ImperoFiere | Organizziamo e ospitiamo i vostri eventi fieristici" />
    <meta name="author" content="Andrea Cardin, Andrea Nalesso, Gabriele Marcomin, Ismaele Gobbo" />
    <meta name="description" content="Home Page del sito di ImperoFiere, societa' fieristica di Rovigo" />
    <meta name="keywords" content="index, ImperoFiere, fiera, Rovigo, Impero" />
    <meta name="language" content="italian it" />
  </xsl:template>

</xsl:stylesheet>