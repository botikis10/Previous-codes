<!-- resources/views/admin/vehicle/edit.blade.php -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Gépjármű szerkesztése</title>
</head>
<body>
    <h1>Gépjármű szerkesztése</h1>

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

    <form action="{{ route('vehicle.update', $vehicle->id) }}" method="POST" enctype="multipart/form-data">
        @csrf
        @method('PUT')

        <label for="plate_number">Rendszám:</label>
        <input type="text" id="plate_number" name="plate_number" value="{{ $vehicle->plate_number }}" disabled>

        <label for="brand">Márka:</label>
        <input type="text" id="brand" name="brand" value="{{ $vehicle->brand }}" required>

        <label for="type">Típus:</label>
        <input type="text" id="type" name="type" value="{{ $vehicle->type }}" required>

        <label for="type">Gyártási év:</label>
        <input type="text" id="manufacture_year" name="manufacture_year" value="{{ $vehicle->manufacture_year }}" required>

        <label for="image">Kép módosítása:</label>
        <input type="file" id="image" name="image" accept="image/jpeg,image/png,image/jpg,image/gif">

        <button type="submit">Mentés</button>
    </form>


</body>
</html>