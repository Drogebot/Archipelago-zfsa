<?php
$file = file_get_contents("static_logic.py");

$matches = [];
preg_match_all('/BASE_LOCATION_OFFSET\\+\\d+/m', $file, $matches, PREG_SET_ORDER, 0);

echo count($matches);

for($i = 0; $i < count($matches); $i++)
{
	$file = preg_replace('/BASE_LOCATION_OFFSET\\+\\d+/m', "BASE_LOCATION_TESFFO+{$i}", $file, 1);
}
$file = preg_replace('/BASE_LOCATION_TESFFO/m', "BASE_LOCATION_OFFSET", $file);

file_put_contents("static_logic.py", $file);