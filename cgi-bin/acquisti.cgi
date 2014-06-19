#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use CGI::Session();
use HTML::Template;


#print "Content-type: text/html\n\n";

# $login{"level"} indica il livello di accessibilita' dell'utente ( 0 = non loggato, 1 = utente, 2 = admin)

#creo il template
my $templateName = 'acquisti.tmpl';
my $template     = HTML::Template->new(filename=>'acquisti.tmpl');
# 

# 
# my $session = CGI::Session->load();
# my $sessionname = $session->param('utente');
# 
# if ($sessionname ne "") {  #l'utente è già loggato

$page = new CGI;

  #print $page->header(-location => "$ENV{HTTP_REFERER}"); # redirect alla pagina che ha richiesto il login
#Per poter partecipare all'evento bisogna essere registrati : 
# Attenzione : è necessario essere loggati 


# }
# else {
# 
# } // il nome dovrà essere prelevato da 

$file_acquisti = 'acquisti.xml';
$ns_uri  = 'http://www.imperofiere.com';
$ns_abbr = 'd';

#espressioni xpath
my $ticketTypesXPath = "/${ns_abbr}:acquisti/${ns_abbr}:tipologia/\@id";

#messaggi errore
$parsing_err     = "Operazione di parsing fallita";
$access_root_err = "Impossibile accedere alla radice";

#creo il parser
my $parser = XML::LibXML->new();

#parser del documento
my $doc = $parser->parse_file($file_acquisti) || die($parsing_err);

#recupero l'elemento radice
my $root_acq = $doc->getDocumentElement || die($access_root_err);

#inserisco il namespace
$doc->documentElement->setNamespace($ns_uri,$ns_abbr);

my @tipiBiglietti = $root_acq->findnodes($ticketTypesXPath);

# foreach my $tipoBiglietti (@tipibiglietto) { print $tipoBiglietti->getValue() ."<br />"; } #http://html-template.sourceforge.net/html_template.html#tmpl_loop



my @loop_data = ();  # initialize an array to hold your loop


foreach my $tipoBiglietto ( @tipiBiglietti) {
	 my %row_data;  # get a fresh hash for the row data
	  # fill in this row
	 $row_data{TIPIBIGLIETTI} =  $tipoBiglietto->getValue();
	 
	 # the crucial step - push a reference to this row into the loop!
	 push(@loop_data, \%row_data);
}
	 
# finally, assign the loop data to the loop param, again with a
# reference:
$template->param(LOOP_TIPIBIGLIETTI => \@loop_data);

HTML::Template->config(utf8 => 1);
print "Content-Type: text/html\n\n", $template->output;


# print << "EOF"
# 
# EOF
# ;