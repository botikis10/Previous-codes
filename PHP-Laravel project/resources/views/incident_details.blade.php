<!-- resources/views/incident_details.blade.php -->

<!DOCTYPE html>
<html>
<head>
    <title>Káresemény részletező</title>
</head>
<body>

    <!-- Vissza a főoldalra -->
    <a href="/">
        <button style="position: absolute; top: 10px; right: 10px;">Vissza a főoldalra</button>
    </a>

    @if(isset($error))
        <p>{{ $error }}</p>
    @else
        <h1>Káresemény részletei</h1>
        <h2>Dátum: {{ $incident->date_time }}</h2>
        <p>Helyszín: {{ $incident->location }}</p>
        <!-- További káresemény adatok -->

        <h2>Járművek részletei:</h2>
        @foreach($incident->vehicles as $vehicle)
            <div>
                <h3>Rendszám: {{ $vehicle->plate_number }}</h3>
                <p>Márka: {{ $vehicle->brand }}</p>
                <p>Típus: {{ $vehicle->type }}</p>
                <!-- További jármű adatok -->

                @if($vehicle->image)
                    @if (Str::startsWith($vehicle->image, ['http://', 'https://']))
                        <img src="{{ $vehicle->image }}" alt="Vehicle Image" width="200">
                    @else
                        <img src="{{ asset('storage/' . $vehicle->image) }}" alt="Vehicle Image" width="200">
                    @endif
                @else
                    <p>Kép nem elérhető</p>
                @endif
            </div>
            <hr>
        @endforeach
    @endif
</body>
</html>