<!-- all_plate_numbers.blade.php -->

<!DOCTYPE html>
<html>
    <head>
        <title>Minden rendszám</title>
    </head>
    <body>
        <h1>Minden rendszám</h1>

        @foreach($allVehicles as $plateNumber)
            {{ $plateNumber }} <br>
        @endforeach

    </body>
</html>
