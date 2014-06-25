#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use Digest::SHA qw(sha256_hex);
use CGI::Session();
use HTML::Template;

$page = new CGI;

my $session = CGI::Session->load();
my $sessionname = $session->param('utente');

if ($sessionname ne "") {  #l'utente è già loggato
  print $page->header(-location => "$ENV{HTTP_REFERER}"); # redirect alla pagina che ha richiesto il login
}
else {
  $filedati = "../data/utenti.xml";

  #creo il parser
  $parser = XML::LibXML -> new();

  #apro il file
  $doc = $parser->parse_file($filedati) || die ("operazione di parsificazione fallita.");

  #leggo la radice
  $root = $doc->getDocumentElement || die("Accesso alla radice fallito.");


  my $username = $page->param('username');
  my $password = $page->param('password');
  my $submitted = $page->param('submitted');

  my $success = 0;
  my $strerr = "";

  if ($submitted == 1) {

    $referrer = $page->param('referrer');

    my $hashedpwd = sha256_hex("$password");
    
    $success = $root->exists("//utente[nickname='$username' and password='$hashedpwd']");
    if ($success == 0) {
      $strerr .= "Username o password errati. <br />"; 
    }
  }
  else {
    # tengo traccia della pagina che ma mandato l'uente alla form di login per il redirect
    $riferimento = $ENV{HTTP_REFERER};
  }

  if ($success) {
    $session = new CGI::Session();
    $session->param('utente', $username);
    print $session->header(-location=>"$referrer");

  #   $template->param(SUCCESS => 1);
  #   $template->param(REFER => $referrer);
  }
  else {
    my $template = HTML::Template->new(filename => 'template/index.tmpl');
    $template->param(ERRORE => $strerr);
    $template->param(RIFE => $riferimento);
    
    HTML::Template->config(utf8 => 1);
    print "Content-Type: text/html\n\n", $template->output;
  }
}
# HTML::Template->config(utf8 => 1);
# print "Content-Type: text/html\n\n", $template->output;