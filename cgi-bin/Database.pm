#!/usr/bin/perl -w

use strict; 
use warnings; 
use diagnostics;
use XML::LibXML;


my $parser=XML::LibXML->new();
my $padiglioni='/data/padiglioni/padiglioni.xml';



sub getPad4id{
  my $doc=$parser->parse_file($padiglioni);
  my $root = $doc->getDocumentElement;
  my $idpad=$doc->findnodes("/padiglioni/padiglioni[@id='".$_[0]."']")->get_node(1);
  my @result = $idpad->getElementsByTagName('padiglione');
  return @result;
}
