<!-- resources/views/search_results.blade.php -->
<!DOCTYPE html>
<html>
<head>
    <title>Keresési Eredmények</title>
</head>
<body>
    <h1>Keresési Eredmények</h1>

    <!-- Vissza a főoldalra -->
    <a href="/">
        <button style="position: absolute; top: 10px; right: 10px;">Vissza a főoldalra</button>
    </a>

    @if(session('error'))
        <p style="color: red;">{{ session('error') }}</p>
    @endif

    @if ($vehicle)
        <h2>{{ $vehicle->plate_number }} adatai:</h2>
        <p>Márka: {{ $vehicle->brand }}</p>
        <p>Típus: {{ $vehicle->type }}</p>
        <p>Gyártási év: {{ $vehicle->manufacture_year }}</p>

        <!-- Kép megjelenítése -->
        @if ($vehicle->image)
            @if (Str::startsWith($vehicle->image, ['http://', 'https://']))
                <img src="{{ $vehicle->image }}" alt="Vehicle Image" width="200">
            @else
                <img src="{{ asset('storage/' . $vehicle->image) }}" alt="Vehicle Image" width="200">
            @endif
        @else
            <p>Kép nem található.</p>
        @endif

        @if ($incidents->isNotEmpty())
            <h3>Káresemények:</h3>
            <table>
                <thead>
                    <tr>
                        <th>Helyszín</th>
                        <th>Időpont</th>
                        <th>Leírás</th>
                    </tr>
                </thead>
                <tbody>
                    @foreach ($incidents as $incident)
                        <tr>
                            <td>{{ $incident->location }}</td>
                            <td>{{ $incident->date_time }}</td>
                            <td>{{ $incident->description }}</td>
                            <!-- Káreseményre kattintás -->
                            <td><a href="{{ route('incident_details', $incident->id) }}">Részletek</a></td>
                            
                        </tr>
                    @endforeach
                </tbody>
            </table>
        @else
            <p>Nincsenek káresemények ehhez a járműhöz.</p>
        @endif
    @else
        <p>Nincs találat a rendszámra.</p>
    @endif
</body>
</html>