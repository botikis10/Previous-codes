<!-- resources/views/search_histories/search_histories.blade.php -->

<!DOCTYPE html>
<html>
<head>
    <title>Keresési előzmények</title>
</head>
<body>
    <h1>Keresési előzmények</h1>

    <!-- Vissza a főoldalra -->
    <a href="/">
        <button style="position: absolute; top: 10px; right: 10px;">Vissza a főoldalra</button>
    </a>

    @foreach($searchHistory as $history)
        <div>
            <p>Rendszám: {{ $history->searched_plate_number }}</p>
            <p>Keresés ideje: {{ $history->search_time }}</p>
            <!-- Jármű miniatűr képe, ha rendelkezésre áll -->
            @php
                $vehicle = \App\Models\Vehicle::where('plate_number', $history->searched_plate_number)->first();
            @endphp

            @if($vehicle && $vehicle->image)
                @if (Str::startsWith($vehicle->image, ['http://', 'https://']))
                    <img src="{{ $vehicle->image }}" alt="Vehicle Image" width="200">
                @else
                    <img src="{{ asset('storage/' . $vehicle->image) }}" alt="Vehicle Image" width="200">
                @endif
            @else
                <p>Kép nem elérhető</p>
            @endif

            <!-- Újra keresés -->
            <form method="POST" action="/submit">
                @csrf
                <input type="hidden" name="plate_number" value="{{ $history->searched_plate_number }}">
                <button type="submit">Újra keresés</button>
            </form>

        </div>
        <hr>
    @endforeach

    <!-- Lapozó hozzáadása -->
    {{ $searchHistory->links('vendor.pagination.simple-default') }}
</body>
</html>