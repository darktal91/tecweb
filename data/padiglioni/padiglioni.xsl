<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns="http://www.imperofiere.com" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version='1.0' encoding='UTF-8' indent='yes'/>
    <xsl:template match="/">
        <html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it">
            <head>
	            <title>TheEmpireCon.it - Padiglioni</title>
	            <xsl:call-template name="meta" />
            </head>
            <body>
	            <xsl:call-template name="header"/>
                <div id="posizione">Ti trovi in: Home > Padiglioni</div>
	            <div id="corpo">
                    <xsl:call-template name="nav" />
                    <div id="contenuto">
	                    <xsl:apply-templates select="padiglioni"/>
                    </div>
	            </div>
	            <xsl:call-template name="footer" />
            </body>
        </html>
  </xsl:template>
  
  
  
  <!--Lista di template da chiamare-->
  
  
    <xsl:template match="padiglioni">
        <div id="mappa"><xsl:copy-of select="img"/></div>
        <table id="padiglioni" summary="In questa tabella sono contenuti la lista dei padiglioni, la relativa posizione e l'eventuale evento in corso per padiglione">
            <thead>
	            <tr>
	                <th scope="col">ID</th>
	                <th scope="col">Posizione</th>
	                <th scope="col">Evento in corso</th>
	            </tr>
            </thead>
            <tbody>
	            <xsl:apply-templates select="padiglione"/>
            </tbody>
        </table>
    </xsl:template>
  
    <xsl:template match="padiglione">
        <tr>
            <td><xsl:value-of select="@id" /></td>
            <td><xsl:value-of select="posizione" /></td>
            <td>ci va l'evento</td>
        </tr>
    </xsl:template>
  
    <xsl:template name="meta">
        <link type="text/css" rel="stylesheet" href="../css/stile.css" media="handheld, screen" />
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>TheEmpireCon.it - Padiglioni</title>
        <meta name="title" content="Home Page - ImperoFiere | Organizziamo e ospitiamo i vostri eventi fieristici" />
        <meta name="author" content="Andrea Cardin, Andrea Nalesso, Gabriele Marcomin, Ismaele Gobbo" />
        <meta name="description" content="Home Page del sito di The Empire Con, societa' fieristica di Rovigo" />
        <meta name="keywords" content="index, Empire Con, Con, Rovigo, Empire" />
        <meta name="language" content="italian it" />
    </xsl:template>
  
    <xsl:template name="header">
        <div id="header">
            <div id="logo" >
                <img src="../image/impero.png" />
            </div>
        </div>
    </xsl:template>
  
    <xsl:template name="nav">
        <div id="nav">
            <ul tabindex="1">
                <li><a accesskey="h" href="../index.html">Home</a></li>
                <li><a accesskey="e" href="eventi.cgi">Eventi</a></li>
            <li><a accesskey="p" href="">Padiglioni</a></li>
            <li><a accesskey="d" href="../dovesiamo.html">Dove siamo</a></li>
            <li><a accesskey="c" href="../contatti.html">Contatti</a></li>
            <li><a accesskey="u" href="../areautente.html">Il mio account</a></li>
        </ul>
    </div>
  </xsl:template>
  
  <xsl:template name="footer">
    <div id="footer">
      <a href="http://validator.w3.org/check?uri=referer"><img
	src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" class="footimg"/></a>
      <span id="rights">TheEmpireCon - 2014</span>
      <!--<img src="http://www.w3.org/Icons/valid-css-blue.png" class="footimg" alt="W3C CSS valid" />
	  questa la aggiungeremo quando il validatore ci darà il permesso :P -->
    </div>
  </xsl:template>
</xsl:stylesheet>