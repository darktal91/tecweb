<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:a="http://www.imperofiere.com"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version='1.0' encoding='UTF-8' indent='yes'/>
<xsl:template match="/">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <head>
    <title>Prova</title>
  </head>
  <body>
  <h1>Situazione attuale della vendita dei biglietti</h1>
  <xsl:for-each select="biglietti/biglietto">
    <table>
      <tr>
	<td>Tipo</td>
	<td>Quantità totale</td>
	<td>Venduti</td>
	<td>Prezzo</td>
      </tr>
      <tr>
	<td><xsl:value-of select="@tipo"/></td>
	<td><xsl:value-of select="qtatot"/></td>
	<td><xsl:value-of select="venduti"/></td>
	<td><xsl:value-of select="@prezzo"/></td>
      </tr>
    </table>
    <br />
  </xsl:for-each>
  </body>


</html>
</xsl:template>
</xsl:stylesheet> 
