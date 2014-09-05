#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use CGI::Session();
use HTML::Template;
use Digest::SHA qw(sha256_hex);

my $page = new CGI;
my $templatePage = "template/page.tmpl";
my $templateHeader = "template/header.tmpl";
my $templateFooter = "template/footer.tmpl";
my $templateContent= "template/bodies/areautente.tmpl";
my $file_padiglioni = "../data/padiglioni/padiglioni.xml";
my $ns_uri  = 'http://www.empirecon.it';
# creo il template

my $temp = HTML::Template->new(filename=>$templatePage);

$temp->param(HEADER=>qq/<TMPL_INCLUDE name = "$templateHeader">/);
$temp->param(PATH=>"Home >> Dati personali");
$temp->param(UTENTE=>0);
$temp->param(CONTENUTO=>qq/<TMPL_INCLUDE name = "$templateContent">/);
$temp->param(FOOTER=>qq/<TMPL_INCLUDE name = "$templateFooter">/);

#compilazione template
my $template = new  HTML::Template(scalarref => \$temp->output());
$template->param(PAGE => "Dati personali");
$template->param(KEYWORD => "dati personali, dati utente, EmpireCon, fiera, Impero, Star Wars, convention");
# controllo che l'utente abbia effettuato l'accesso
$session = CGI::Session->load();

my $username = $session->param(-name => 'utente');

if ($username eq "") {      #l'utente non è loggato, lo mando alla form di login
  print $page->header(-location => 'login.cgi');
}
else {       #l'utente è loggato

  $filedati = "../data/utenti/utenti.xml";

  #creo il parser
  $parser = XML::LibXML -> new();

  #apro il file
  $doc = $parser->parse_file($filedati) || die ("operazione di parsificazione fallita.");

  #leggo la radice
  $root = $doc->getDocumentElement || die("Accesso alla radice fallito.");

  $doc->documentElement->setNamespace($ns_uri);

  #il parametro modifica indica:
  # 0 => primo accesso
  # 1 => modifica dati personali
  # 2 => imposta nuova password
  my $modifica = 0;
  $modifica = $page->param('modifica');

  #submitted=1 significa che una form è stata inviata, quindi devo controllare i dati inseriti
  my $submitted = 0;
  $submitted = $page->param('submitted');

  #creo hash per contenere i dati
  my %dati;

  #se modifica è uguale a 0 o a 1 devo caricare tutti i dati personali
  if ($modifica == 0 or $modifica == 1) {
    #estraggo i dati da xml
    my $results = $root->findnodes("//utente[nickname='$username']");
    my $context = $results->get_nodelist;
    foreach my $context ($results->get_nodelist) {
      $dati{"nome"} =  $context->findvalue("nome");
      $dati{"cognome"} =  $context->findvalue("cognome");
      $dati{"datanascita"} =  $context->findvalue("datanascita");
      $dati{"via"} =  $context->findvalue("indirizzo/via");
      $dati{"numero"} =  $context->findvalue("indirizzo/numero");
      $dati{"citta"} =  $context->findvalue("indirizzo/citta");
      $dati{"provincia"} =  $context->findvalue("indirizzo/provincia");
      $dati{"cap"} =  $context->findvalue("indirizzo/CAP");
      $dati{"email"} =  $context->findvalue("email");
    }
    # passo i dati al template
    $template->param(NOME => $dati{"nome"});
    $template->param(COGNOME => $dati{"cognome"});
    $template->param(DATANASCITA => $dati{"datanascita"});
    $template->param(VIA => $dati{"via"});
    $template->param(NUMERO => $dati{"numero"});
    $template->param(CITTA => $dati{"citta"});
    $template->param(PROVINCIA => $dati{"provincia"});
    $template->param(CAP => $dati{"cap"});
    $template->param(EMAIL => $dati{"email"});
  }

  $template->param(USERNAME => $username);

  if ($modifica == 0) {  #è il primo accesso
    $template->param(ZERO => 1);
    $template->param(UNO => 0);

  }
  elsif ($modifica == 1) {   #modifica dei dati personali
    $template->param(ZERO => 0);
    $template->param(UNO => 1);

    if ($submitted) {   # devo controllare i dati inseriti
      # recupero i dati inseriti
      my %cambiati;
      $cambiati{"nome"}=$page->param('nome');
      $cambiati{"cognome"}=$page->param('cognome');
      $cambiati{"datanascita"}=$page->param('datanascita');
      $cambiati{"via"}=$page->param('via');
      $cambiati{"numero"}=$page->param('numero');
      $cambiati{"citta"}=$page->param('citta');
      $cambiati{"provincia"}=$page->param('provincia');
      $cambiati{"cap"}=$page->param('cap');
      $cambiati{"email"}=$page->param('email');

      $errori = 0;
      $strerr = "";

      if ($cambiati{"nome"} ne $dati{"nome"}) { # controllo sul nome
	if ($cambiati{"nome"} eq "") {
	  $errori = 1;
	  $strerr .= "Il campo nome non può essere vuoto.<br />";
	}
      }

      if ($cambiati{"cognome"} ne $dati{"cognome"}) {  # controllo sul cognome
	if ($cambiati{"cognome"} eq "") {
	  $errori = 1;
	  $strerr .= "Il campo cognome non può essere vuoto.<br />";
	}
      }

      if ($cambiati{"datanascita"} ne $dati{"datanascita"}) {  # controllo sulla data di nascita
	if ($cambiati{"datanascita"} eq "") {
	  $errori = 1;
	  $strerr .= "Il campo data di nascita non può essere vuoto.<br />";
	}
	if ($cambiati{"datanascita"} !~ /^((19|20)\d{2})\-(0[1-9]|1[012])-(0[1-9]|[12]\d|3[01])$/) {
      #   la data non ha un formato valido
	  $errori = 1;
	  $strerr .= "Data inserita non valida.<br />";
	}
	else { #la data è nel formato corretto.
	  #controllo sensatezza
	  my($cd, $cm, $cy)=(localtime())[3,4,5];
	  $cm += 1;
	  $cy += 1900;
	  if ($1 > $cy or ($1 == $cy and $3 > $cm) or ($1 == $cy and $3 == $cm and $4 > $cd)) {
	    #la data non ha senso.
	    $errori = 1;
	    $strerr .= "Data inserita non valida.<br />";
	  }
	  else { #la data è sensata, controllo esistenza giorno-mese
	    #se il giorno è 31 controllo che il mese sia formato da 31 giorni
	    if ($4 == 31 and ($3 == 4 or $3 == 6 or $3 == 9 or $3 == 11)) {
	      #giorno 31 in un mese da 30 giorni. errore.
	      $errori = 1;
	      $strerr .= "Data inserita non valida.<br />";
	    }
	    #controllo se il mese è febbraio
	    elsif ($3 == 2) {
	      #controllo se il giorno è 30 o 31
	      if ($4 >= 30) {
		# febbraio non ha i giorni 30 e 31, errore.
		$errori = 1;
		$strerr .= "Data inserita non valida.<br />";
	      }
	      #controllo se il giorno è 29 ma l'anno non è bisestile
	      elsif ($4 == 29 and not (($1 % 400) == 0 or (($1 % 100) != 0 and ($1 % 4) == 0))) {
		#giorno 29 febbraio in un anno NON bisestile, errore.
		$errori = 1;
		$strerr .= "Data inserita non valida.<br />";
	      }
	    }
	  }
	}
      }

      if ($cambiati{"via"} ne $dati{"via"}) { # controllo sulla via
	if ($cambiati{"via"} eq "") {
	  $errori = 1;
	  $strerr .= "Il campo via non può essere vuoto.<br />";
	}
      }

      if ($cambiati{"numero"} ne $dati{"numero"}) {  # controllo sul numero
	if ($cambiati{"numero"} eq "") {
	  $errori = 1;
	  $strerr .= "Il campo numero non può essere vuoto.<br />";
	}
      }

      if ($cambiati{"citta"} ne $dati{"citta"}) {  # controllo sulla città
	if ($cambiati{"citta"} eq "") {
	  $errori = 1;
	  $strerr .= "Il campo città non può essere vuoto.<br />";
	}
      }

      if ($cambiati{"provincia"} ne $dati{"provincia"}) {  # controllo sulla provincia
	if ($cambiati{"provincia"} eq "") {
	  $errori = 1;
	  $strerr .= "Il campo provincia non può essere vuoto<br />";
	}
	else {
	  my @province = ('AG', 'AL', 'AN', 'AO', 'AR', 'AP', 'AT', 'AV', 'BA', 'BT', 'BL', 'BN', 'BG', 'BI', 'BO', 'BZ', 'BS', 'BR', 'CA', 'CL', 'CB', 'CI', 'CE', 'CT', 'CZ', 'CH', 'CO', 'CS', 'CR', 'KR', 'CN', 'EN', 'FM', 'FE', 'FI', 'FG', 'FC', 'FR', 'GE', 'GO', 'GR', 'IM', 'IS', 'SP', 'AQ', 'LT', 'LE', 'LC', 'LI', 'LO', 'LU', 'MC', 'MN', 'MS', 'MT', 'ME', 'MI', 'MO', 'MB', 'NA', 'NO', 'NU', 'OT', 'OR', 'PD', 'PA', 'PR', 'PV', 'PG', 'PU', 'PE', 'PC', 'PI', 'PT', 'PN', 'PZ', 'PO', 'RG', 'RA', 'RC', 'RE', 'RI', 'RN', 'RM', 'RO', 'SA', 'VS', 'SS', 'SV', 'SI', 'SR', 'SO', 'TA', 'TE', 'TR', 'TO', 'OG', 'TP', 'TN', 'TV', 'TS', 'UD', 'VA', 'VE', 'VB', 'VC', 'VR', 'VV', 'VI', 'VT');
	  unless (grep {$cambiati{"provincia"} eq $_} @province) {
	    $errori = 1;
	    $strerr .= "Provincia inserita non valida.<br />";
	  }
	}
      }

      if ($cambiati{"cap"} ne $dati{"cap"}) {  # controllo sul cap
	if ($cambiati{"cap"} eq "") {
	  $errori = 1;
	  $sterr .= "Il campo CAP non può essere vuoto<br />";
	}
	 elsif ($cambiati{"cap"} !~ /^[0-9]{5}$/) {
	   $errori = 1;
	   $strerr .= "CAP inserito non valido<br />";
	 }
      }

      if ($cambiati{"email"} ne $dati{"email"}) {  # controllo sull'email
	if ($cambiati{"email"} eq "") {
	  $errori = 1;
	  $strerr .= "Il campo <span xml:lang=\"en\">email</span> non può essere vuoto.<br />";
	}
	elsif ($cambiati{"email"} !~ /^([\w\.\-]+)@([A-Za-z0-9\.\-]*[a-zA-Z0-9])\.([a-zA-Z]{2,4})$/) {
	  $errori = 1;
	  $strerr .= "<span xml:lang=\"en\">email</span> inserita non valida.<br />";
	}
      }

      if ($errori == 1) {  # i dati inseriti non sono validi
	$template->param(OK => 0);
	$template->param(STRERR => $strerr);
	$template->param(NOME => $cambiati{"nome"});
	$template->param(COGNOME => $cambiati{"cognome"});
	$template->param(DATANASCITA => $cambiati{"datanascita"});
	$template->param(VIA => $cambiati{"via"});
	$template->param(NUMERO => $cambiati{"numero"});
	$template->param(CITTA => $cambiati{"citta"});
	$template->param(PROVINCIA => $cambiati{"provincia"});
	$template->param(CAP => $cambiati{"cap"});
	$template->param(EMAIL => $cambiati{"email"});
      }
      else {  # i dati inseriti sono validi, procedo alla modifica

	#nome
	my $modnome = $doc->findnodes("//utente[nickname='$username']/nome/text()")->get_node(1) or die("fallimento nel recupero del nodo per la modifica");
	$modnome->setData("$cambiati{'nome'}");

	#cognome
	my $modcognome = $doc->findnodes("//utente[nickname='$username']/cognome/text()")->get_node(1) or die("fallimento nel recupero del nodo per la modifica");
	$modcognome->setData("$cambiati{'cognome'}");

	#datanascita
	my $moddatanascita = $doc->findnodes("//utente[nickname='$username']/datanascita/text()")->get_node(1) or die("fallimento nel recupero del nodo per la modifica");
	$moddatanascita->setData("$cambiati{'datanascita'}");

	#via
	my $modvia = $doc->findnodes("//utente[nickname='$username']/indirizzo/via/text()")->get_node(1) or die("fallimento nel recupero del nodo per la modifica");
	$modvia->setData("$cambiati{'via'}");

	#numero
	my $modnumero = $doc->findnodes("//utente[nickname='$username']/indirizzo/numero/text()")->get_node(1) or die("fallimento nel recupero del nodo per la modifica");
	$modnumero->setData("$cambiati{'numero'}");

	#citta
	my $modcitta = $doc->findnodes("//utente[nickname='$username']/indirizzo/citta/text()")->get_node(1) or die("fallimento nel recupero del nodo per la modifica");
	$modcitta->setData("$cambiati{'citta'}");

	#provincia
	my $modprovincia = $doc->findnodes("//utente[nickname='$username']/indirizzo/provincia/text()")->get_node(1) or die("fallimento nel recupero del nodo per la modifica");
	$modprovincia->setData("$cambiati{'provincia'}");

	#cap
	my $modcap = $doc->findnodes("//utente[nickname='$username']/indirizzo/CAP/text()")->get_node(1) or die("fallimento nel recupero del nodo per la modifica");
	$modcap->setData("$cambiati{'cap'}");

	#email
	my $modemail = $doc->findnodes("//utente[nickname='$username']/email/text()")->get_node(1) or die("fallimento nel recupero del nodo per la modifica");
	$modemail->setData("$cambiati{'email'}");

	$doc->toFile($filedati) or die("fallimento in scrittura");

	$template->param(OK => 1);
      }

    }
    else {  #submitted=0
      #non è ancora stato fatto submit, mostro i dati dell'xml già passati in precedenza
      $template->param(OK => 0);
    }

  } #fine modifica==1
  elsif ($modifica == 2) {    #imposta nuova password
    $template->param(ZERO => 0);
    $template->param(UNO => 0);

    if ($submitted) {  # è stato fatto il submit, recupero i dati e li controllo
      my %cambiati;
      $cambiati{"oldpwd"}=$page->param("oldpassword");
      $cambiati{"newpwd"}=$page->param("newpassword");
      $cambiati{"cnewpwd"}=$page->param("cnewpassword");
      my $errori = 0;
      my $strerr = "";

      #controllo correttezza della vecchia password
      my $h_oldpwd = sha256_hex("$cambiati{'oldpwd'}");
      my $storedpwd = $doc->findvalue("//utente[nickname='$username']/password");
      if ($h_oldpwd ne $storedpwd) {  # la password inserita è errata
	$errori = 1;
	$strerr .= "La vecchia <span xml:lang=\"en\">password</span> inserita è errata. <br />";
      }
      else {  # la vecchia password inserita è corretta. controllo le nuove password
	if ($cambiati{"newpwd"} eq "") { #controllo che la nbuova password non sia vuota
	  $errori = 1;
	  $strerr .= "La nuova <span xml:lang=\"en\">password</span> non può essere vuota. <br />";
	}
	elsif ($cambiati{"newpwd"} ne $cambiati{"cnewpwd"}) {  # controllo che la nuova password corrisponda a quella di controllo
	  $errori = 1;
	  $strerr .= "La nuova <span xml:lang=\"en\">password</span> inserita è diversa da quella di conrollo. <br />";
	}
	elsif (length($cambiati{"newpwd"}) < 8) {  # controllo che la password sia di almeno 8 caratteri
	  $errori = 1;
	  $strerr .= "<span xml:lang=\"en\">Password</span> troppo corta, sono necessarmi almeno 8 caratteri. <br />";
	}
      }

      # controllo se ci sono errori nella password
      if ($errori == 1) {  #ci sono stati degli errori, trasmetto la stringa di errore
	$template->param(OK => 0);
	$template->param(STRERR => $strerr);
      }
      else {
	# modifico la password nel file xml

	my $h_newpwd = sha256_hex("$cambiati{'newpwd'}");

	my $node = $doc->findnodes("//utente[nickname='$username']/password/text()")->get_node(1) or die("fallimento nel recupero del nodo per la modifica");
	$node->setData($h_newpwd);
	$doc->toFile($filedati) or die("fallimento in scrittura");

	$template->param(OK => 1);
      }

    } #fine submit 2
    else {  # non è ancora stato fatto submit
      $template->param(OK => 0);
    }
  } #fine modifica==2
  else {   #parametro di modifica non valido
    die("pagina non trovata");
  }
  HTML::Template->config(utf8 => 1);
  print "Content-Type: text/html\n\n", $template->output;
}
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <link type="text/css" rel="stylesheet" href="css/style.css" media="handheld, screen" />
  <link type="text/css" rel="stylesheet" href="css/handheld.css" media="handheld, screen and (max-width:550px), only screen and (max-device-width:550px)" />
  <link type="text/css" rel="stylesheet" href="css/print.css" media="print" />
  <title>Dati personali | EmpireCon</title>
  <meta name="title" content="Dati personali | EmpireCon" />
  <meta name="author" content="Andrea Cardin, Andrea Nalesso, Gabriele Marcomin, Ismaele Gobbo" />
  <meta name="description" content="Visualizzazione dei dati personali dell'utente del sito di EmpireCon, convention su Star Wars" />
  <meta name="keywords" content="" />
  <meta name="language" content="italian it" />
</head>
