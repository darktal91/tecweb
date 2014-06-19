#!/usr/bin/perl

# import required modules
use XML::XSLT;

# define local variables
my $xslfile = "../data/padiglioni/padiglioni.xsl";
my $xmlfile = "../data/padiglioni/padiglioni.xml";

# create an instance of XSL::XSLT processor
my $xslt = XML::XSLT->new ($xslfile);

# transform XML file and print output
print $xslt->serve($xmlfile);

# free up some memory
$xslt->dispose(); 