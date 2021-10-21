<?php
$address = htmlspecialchars($_GET["ip"]);
$socket = fsockopen($address, "23", $errno, $errstr);

if($socket)
{
    echo "Connected <br /><br />";
}
else
{
    echo "Connection failed!<br /><br />";
}

fputs($socket, "REBOOT \r\n{Enter}");

$buffer = "";

while(!feof($socket))
{
    $buffer .=fgets($socket, 4096);
}

print_r($buffer);
echo "<br /><br /><br />";
var_dump($buffer);

fclose($socket);
?>
