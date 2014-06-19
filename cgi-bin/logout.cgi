#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session();

my $page = new CGI;

my $session = CGI::Session->load() or die ("caricamento della sessione fallito");
$session->close();
$session->delete();
$session->flush();

print $page->header(-location => 'index.cgi');