#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use Digest::SHA qw(sha256_hex);
use HTML::Template;

my $page = new CGI;

my $filedati = "../data/utenti.xml";

#creo il parser
my $parser = XML::LibXML -> new();

#apro il file
my $doc = $parser -> parse_file($filedati) || die ("operazione di parsificazione fallita.");

#leggo la radice
my $root = $doc->getDocumentElement || die("Accesso alla radice fallito.");

sub chk_username {
  my $x = lc($_[0]);
  if ($x eq "") {
    $errori{"nickname"} = 1;
    $sterr .= "L'username non può essere vuoto.<br />";
  }
  else {
    @usernames = $root->getElementsByTagName("nickname");
    if (grep { $x eq lc($_->getFirstChild->getData) } @usernames) {
      $errori{"nickname"} = 1;
      $sterr .= "L'username inserito è già esistente.<br />";
    }
  }
}

sub chk_pwd {
  my $p = $_[0];
  my $c = $_[1];
  
  if ($p eq "") {
    $errori{"password"} = 1;
    $sterr .= "Il campo password non può essere vuoto.<br />";
  }
  elsif ($p ne $c) {
    $errori{"password"} = 1;
    $sterr .= "La due password inserite non corrispondono.<br />";
  }
  elsif (length($p) < 8) {
    $errori{"password"} = 1;
    $sterr .= "Password troppo corta, sono necessari almeno 8 caratteri.<br />";
  }
}

sub chk_nome {
  if ($_[0] eq "") {
    $errori{"nome"} = 1;
    $sterr .= "Il campo nome non può essere vuoto.<br />";
  }
}

sub chk_cognome {
  if ($_[0]eq "") {
    $errori{"cognome"} = 1;
    $sterr .= "Il campo cognome non può essere vuoto.<br />";
  }
}

sub chk_via {
  if ($_[0]eq "") {
    $errori{"via"} = 1;
    $sterr .= "Il campo via non può essere vuoto.<br />";
  }
}

sub chk_numero {
  if ($_[0]eq "") {
    $errori{"numero"} = 1;
    $sterr .= "Il campo numero non può essere vuoto.<br />";
  }
}

sub chk_citta {
  if ($_[0]eq "") {
    $errori{"citta"} = 1;
    $sterr .= "Il campo citta non può essere vuoto.<br />";
  }
}


sub chk_datanascita {
  my $d = $_[0];
  
  if ($d eq "") {
    $errori{"datanascita"} = 1;
    $sterr .= "Il campo data di nascita non può essere vuoto.<br />";
  }
  if ($d !~ /^((19|20)\d{2})\-(0[1-9]|1[012])-(0[1-9]|[12]\d|3[01])$/) { 
#   la data non ha un formato valido
    $errori{"datanascita"} = 1;
    $sterr .= "Data inserita non valida.<br />";
  }
  else { #la data è nel formato corretto. 
    #controllo sensatezza
    my($cd, $cm, $cy)=(localtime())[3,4,5];
    $cm += 1;
    $cy += 1900;
    if ($1 > $cy or ($1 == $cy and $3 > $cm) or ($1 == $cy and $3 == $cm and $4 > $cd)) {
      #la data non ha senso.
      $errori{"datanascita"} = 1;
      $sterr .= "Data inserita non valida.<br />";
    }
    else { #la data è sensata, controllo esistenza giorno-mese
      #se il giorno è 31 controllo che il mese sia formato da 31 giorni
      if ($4 == 31 and ($3 == 4 or $3 == 6 or $3 == 9 or $3 == 11)) {
	#giorno 31 in un mese da 30 giorni. errore.
	$errori{"datanascita"} = 1;
	$sterr .= "Data inserita non valida.<br />";
      }
      #controllo se il mese è febbraio
      elsif ($3 == 2) {
	#controllo se il giorno è 30 o 31
	if ($4 >= 30) {
	  # febbraio non ha i giorni 30 e 31, errore.
	  $errori{"datanascita"} = 1;
	  $sterr .= "Data inserita non valida.<br />";
	}
	#controllo se il giorno è 29 ma l'anno non è bisestile
	elsif ($4 == 29 and not (($1 % 400) == 0 or (($1 % 100) != 0 and ($1 % 4) == 0))) {
	  #giorno 29 febbraio in un anno NON bisestile, errore.
	  $errori{"datanascita"} = 1;
	  $sterr .= "Data inserita non valida.<br />";
	}
      } 
    }
  }
}

sub chk_provincia {
  my $x = uc($_[0]);
  if($x eq "") {
    $errori{"provincia"} = 1;
    $sterr .= "Il campo provincia non può essere vuoto<br />";
  }
  else {
    my @province = ('AG', 'AL', 'AN', 'AO', 'AR', 'AP', 'AT', 'AV', 'BA', 'BT', 'BL', 'BN', 'BG', 'BI', 'BO', 'BZ', 'BS', 'BR', 'CA', 'CL', 'CB', 'CI', 'CE', 'CT', 'CZ', 'CH', 'CO', 'CS', 'CR', 'KR', 'CN', 'EN', 'FM', 'FE', 'FI', 'FG', 'FC', 'FR', 'GE', 'GO', 'GR', 'IM', 'IS', 'SP', 'AQ', 'LT', 'LE', 'LC', 'LI', 'LO', 'LU', 'MC', 'MN', 'MS', 'MT', 'ME', 'MI', 'MO', 'MB', 'NA', 'NO', 'NU', 'OT', 'OR', 'PD', 'PA', 'PR', 'PV', 'PG', 'PU', 'PE', 'PC', 'PI', 'PT', 'PN', 'PZ', 'PO', 'RG', 'RA', 'RC', 'RE', 'RI', 'RN', 'RM', 'RO', 'SA', 'VS', 'SS', 'SV', 'SI', 'SR', 'SO', 'TA', 'TE', 'TR', 'TO', 'OG', 'TP', 'TN', 'TV', 'TS', 'UD', 'VA', 'VE', 'VB', 'VC', 'VR', 'VV', 'VI', 'VT');
    unless (grep {$x eq $_} @province) {
      $errori{"provincia"} = 1;
      $sterr .= "Provincia inserita non valida.<br />";
    } 
  }
}

sub chk_cap {
  my $x = $_[0];
  if ($x eq "") {
    $errori{"cap"} = 1;
    $sterr .= "Il campo CAP non può essere vuoto<br />";
  }
  elsif ($x !~ /^[0-9]{5}$/) {
    $errori{"cap"} = 1;
    $sterr .= "CAP inserito non valido<br />";
  }
}

sub chk_email {
  my $x = $_[0];
  if ($x eq "") {
    $errori{"email"} = 1;
    $sterr .= "Il campo email non può essere vuoto.<br />";
  }
  elsif ($x !~ /^([\w\.\-]+)@([A-Za-z0-9\.\-]*[a-zA-Z0-9])\.([a-zA-Z]{2,4})$/) {
    $errori{"email"} = 1;
    $sterr .= "email inserita non valida.<br />";
  }
}

%errori=("username" => 0,
	"password" => 0,
	"nome" => 0,
	"cognome" => 0,
	"datanascita" => 0,
	"via" => 0,
	"numero" => 0,
	"citta" => 0,
	"provincia" => 0,
	"cap" => 0,
	"email" => 0
	);

my $strerr = "";
my $ok = 0;
my $submitted = 0;

my $username=$page->param('username');
my $password=$page->param('password');
my $cpassword=$page->param('c_password');
my $nome=$page->param('nome');
my $cognome=$page->param('cognome');
my $datanascita=$page->param('datanascita');
my $via=$page->param('via');
my $numero=$page->param('numero');
my $citta=$page->param('citta');
my $provincia=$page->param('provincia');
my $cap=$page->param('cap');
my $email=$page->param('email');
$submitted=$page->param('submitted');

if($submitted == 1) {
  &chk_username($username);
  &chk_pwd($password, $cpassword);
  &chk_nome($nome);
  &chk_cognome($cognome);
  &chk_datanascita($datanascita);
  &chk_via($via);
  &chk_numero($numero);
  &chk_citta($citta);
  &chk_provincia($provincia);
  &chk_cap($cap);
  &chk_email($email);  
  unless (grep {$_ == 1} values %errori) {
    $ok = 1;
  }
}

# creo il link al template
my $template = HTML::Template->new(filename => 'registrazione.tmpl');

if ($ok == 0) {
  $template->param(OK => 0);
  $template->param(ERRORI => $sterr);
  $template->param(USERNAME => $username);
  $template->param(NOME => $nome);
  $template->param(COGNOME => $cognome);
  $template->param(DATANASCITA => $datanascita);
  $template->param(VIA => $via);
  $template->param(NUMERO => $numero);
  $template->param(CITTA => $citta);
  $template->param(PROVINCIA => $provincia);
  $template->param(CAP => $cap);
  $template->param(EMAIL => $email);
}
else {
  my $hashpwd = sha256_hex("$password");
  $provincia = uc($provincia);
  
  #creo frammento da aggiungere
  my $frammento = "\t<utente>
\t\t<nickname>$username</nickname>
\t\t<password>$hashpwd</password>
\t\t<nome>$nome</nome>
\t\t<cognome>$cognome</cognome>
\t\t<datanascita>$datanascita</datanascita>
\t\t<indirizzo>
\t\t\t<via>$via</via>
\t\t\t<numero>$numero</numero>
\t\t\t<citta>$citta</citta>
\t\t\t<provincia>$provincia</provincia>
\t\t\t<CAP>$cap</CAP>
\t\t</indirizzo>
\t\t<email>$email</email>
\t</utente>\n";


  my $newnodo = $parser->parse_balanced_chunk($frammento) || die("Frammento non ben formato");

  $root->appendChild($newnodo) || die ("non riesco a trovare il padre");

  $doc->toFile($filedati);
  
  $template->param(OK => 1);
}

HTML::Template->config(utf8 => 1);
print "Content-Type: text/html\n\n", $template->output;