#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use Digest::SHA qw(sha256_hex);
use CGI::Session();

# sub createSession() {
#   
# #   print $session->header(-location=>"$base");
# }

$page = new CGI();
$parser = XML::LibXML->new();
$filedati = "../data/utenti/utenti.xml";
$doc = $parser->parse_file($filedati);
$root = $doc->getDocumentElement();
my $success = $root->exists("utente[nickname=\"admin\"]");
print $page->header,
    $page->start_html('hello world'),
    $page->h1("Buongiorno a te",$success),
    $page->end_html;



  

