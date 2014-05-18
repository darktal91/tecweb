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
	<xsl:call-template name="header"/>
	<xsl:call-template name="nav" />
	<div id="contenuto">
	  <xsl:apply-templates select="padiglioni/padiglione"/> 
	</div>
	<xsl:call-template name="footer" />
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
  
  <xsl:template name="header">
    <div id="header">
      <h1>Impero Fiere</h1>
    </div>
  </xsl:template>
  
  <xsl:template name="nav">
    <div id="nav">
      <ul class="menu">
	<li><a href="">Home</a></li>
	<li><a href="eventi.html">Eventi</a></li>
	<li><a href="mappa.html">Mappa Padiglioni</a></li>
	<li><a href="dovesiamo.html">Dove siamo</a></li>
	<li><a href="contatti.html">Contatti</a></li>
      </ul>
    </div>
  </xsl:template>
  
  <xsl:template name="footer">
    <div id="footer">
      <a href="http://validator.w3.org/check?uri=referer"><img
	src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" class="footimg"/></a>
      <span id="rights">ImperoFiere - 2014</span>
      <!--<img src="http://www.w3.org/Icons/valid-css-blue.png" class="footimg" alt="W3C CSS valid" />
	  questa la aggiungeremo quando il validatore ci darà il permesso :P -->
    </div>
  </xsl:template>
</xsl:stylesheet>