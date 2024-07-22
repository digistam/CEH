#!/usr/bin/perl

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Mosucker 2.2 CGI Notification Script. Copyright by Zeloran (zeloran@freenet.de)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

print "Content-Type: text/plain\n\n";                   # Mitteilen dass die Ausgabe im Textformat statt findet

@parameters = split(/&/,$ENV{'QUERY_STRING'});          # Alle Parameter ermitteln und ein ein Array schreiben
foreach $element (@parameters) {                        # Jeden im Array gefundenen Parameter
  ($name, $value) = split(/=/,$element);                # in zwei Variablen f�r Namen und Wert aufteilen
  $value =~ tr/+/ /;                                    # Alle vorkommenen + durch Leerzeichen erseztzen
  $parameter{$name} = $value;                           # eine Hash Variable mit Namen und Wert erzeugen
}

@date = split(/ /, localtime());                        # Das aktuelle Datum ermitteln
@time = split(/:/, @date[3]);                           # Die akuelle Uhrzeit ermitteln

$filename = "$ENV{'DOCUMENT_ROOT'}/cgi-bin/online.txt"; # Der Variablen f�r die Online Liste den Dateinamen zuweisen
$ip = "$ENV{'REMOTE_ADDR'}";                            # Die IP Adresse in einer Variablen speichern

open(IN, $filename);                                    # Die Datei f�r die Online Liste zum Lesen �ffnen
@lines = <IN>;                                          # Den Inhalt der Datei in ein Array einlesen
close(IN);                                              # Den Dateizugriff wieder schlie�en

for($var = 0;$var <= $#lines;$var++) {                  # Jedes Element der Liste auf einen eigenen Eintrag �berpr�fen
  @information = split(/#/, $lines[$var]);              # Die durch "#" getrennten Informationen ermitteln
  if($information[2] eq $ip) {                          # �berpr�fen ob die eigene IP mit dem Eintrag identisch ist
    goto change;                                        # Falls dies der Fall ist Suchdurchlauf abbrechen
  }
}

change: $lines[$var] = "@time[0]#@time[1]#$ip#$parameter{'port'}#$parameter{'nick'}#$parameter{'country'}#$parameter{'visible'}#$parameter{'protected'}#$parameter{'about'} [Last notify: @time[0]:@time[1]]\n";

open(OUT, ">$filename");                                # Die Datei f�r die Online Liste zum Schreiben �ffnen
foreach $element (@lines) {                             # Jedes Element der Liste
  print OUT "$element";                                 # in die Datei schreiben
}
close(OUT);                                             # Den Dateizugriff wieder schlie�en

print "Sweet, Sweet Gwendoline...";                     # Mitteilung an den Server �ber den Erfolg des Eintragens