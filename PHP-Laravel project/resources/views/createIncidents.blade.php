<!-- resources/views/admin/damage_event/createIncidents.blade.php -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Káresemény hozzáadása</title>
</head>
<body>
    <h1>Káresemény hozzáadása!</h1>

    <!-- Vissza a főoldalra -->
    <a href="/">
        <button style="position: absolute; top: 10px; right: 10px;">Vissza a főoldalra</button>
    </a>

    @if ($errors->any())
        <div>
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <form action="{{ route('damage_event.store') }}" method="POST">
        @csrf

        <label for="location">Helyszín:</label>
        <input type="text" id="location" name="location" required><br>

        <label for="date_time">Dátum:</label>
        <input type="datetime-local" id="date_time" name="date_time" required><br>

        <label for="description">Leírás:</label>
        <textarea id="description" name="description"></textarea><br>

        <label for="vehicles">Válasszon járműveket:</label><br>
        @foreach($vehicles as $vehicle)
            <input type="checkbox" id="{{ $vehicle->id }}" name="vehicles[]" value="{{ $vehicle->id }}">
            <label for="{{ $vehicle->id }}">{{ $vehicle->plate_number }}</label><br>
        @endforeach

        <button type="submit">Káresemény létrehozása</button>
    </form>

</body>
</html>