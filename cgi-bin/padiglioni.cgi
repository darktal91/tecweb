#!usr/local/bin/Perl
use CGI;
use XML::LibXSLT;
use XML::LibXML;

my $parser = XML::LibXML->new();
my $xslt = XML::LibXSLT->new();

my $source = $parser->parse_file('../data/padiglioni/padiglioni.xml');
my $style_doc = $parser->parse_file('../data/padiglioni/padiglioni..xsl');
my $stylesheet = $xslt->parse_stylesheet($style_doc);

my $results = $stylesheet->transform($source);
print $stylesheet->output_string($results);