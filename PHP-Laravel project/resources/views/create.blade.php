<!-- resources/views/admin/vehicle/create.blade.php -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Gépjármű hozzáadása</title>
</head>
<body>
    <h1>Gépjármű hozzáadása</h1>

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

    @if(session('error'))
        <p style="color: red;">{{ session('error') }}</p>
    @endif

    @if(session('success'))
        <div class="alert alert-success">
            {{ session('success') }}
        </div><br>
    @endif

    <form action="{{ route('vehicle.store') }}" method="POST" enctype="multipart/form-data">
        @csrf

        <label for="plate_number">Rendszám:</label>
        <input type="text" id="plate_number" name="plate_number" required><br>

        <label for="brand">Márka:</label>
        <input type="text" id="brand" name="brand" required><br>

        <label for="type">Típus:</label>
        <input type="text" id="type" name="type" required><br>

        <label for="type">Gyártási év:</label>
        <input type="text" id="manufacture_year" name="manufacture_year" required><br>

        <label for="image">Kép feltöltése:</label>
        <input type="file" id="image" name="image" required accept="image/jpeg,image/png,image/jpg,image/gif"><br>

        <button type="submit">Mentés</button>
    </form>

</body>
</html>