<!-- resources/views/home.blade.php -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Gépjármű-kártörténet kezelő rendszer</title>
</head>
<body>
    <h1>Üdvözöllek a rendszerben!</h1>
    
    <p> Üdvözöllek a gépjármű-kártörténet kezelő rendszerben!</p>
    <p>A Gépjármű-kártörténet Kezelő Rendszer lehetővé teszi az alábbiak elvégzését:</p>
    <ul>
        <li>Rendszámtábla alapján keresést végezhet és kilistázhatja az autó részletes adatait, valamint azokhoz kapcsolódó káreseményeket.</li>
        <li>Megtekintheti a korábbi keresési előzményeket.</li>
        <li>Hozzáadhat és szerkeszthet járműveket.</li>
        <li>Hozzáadhat, szerkeszthet és törölhet káreseményeket.</li>
        <li>Kezelheti a prémium felhasználókat.</li>
    </ul>

    <!-- Hibaüzenetek megjelenítése -->
    @if(session('error'))
        <p style="color: red;">{{ session('error') }}</p>
    @endif

    @if(session('success'))
        <div style="color: green" class="alert alert-success">
            {{ session('success') }}
        </div><br>
    @endif

    @if(Auth::check())
        <!-- Bejelentkezett felhasználók esetén a kijelentkezés gomb -->
        <form method="POST" action="{{ route('logout') }}">
            @csrf
            <button type="submit">Kijelentkezés</button>
        </form>
    @else
        <!-- Kijelentkezett felhasználók esetén a bejelentkezés gomb -->
        <form method="GET" action="{{ route('register') }}">
            <button type="submit">Bejelentkezés</button>
        </form>
    @endif

    
    <br><form method="POST" action="/submit">
        @csrf
        <label for="plate_number">Rendszám keresése:</label>
        <input type="text" id="plate_number" name="plate_number" placeholder="Pl.: ABC123" required><br>
        <button type="submit">Keresés</button>
    </form>

    <!-- Gomb a keresési előzmények megtekintéséhez -->
    <br><a href="{{ route('search_history') }}">
    <button>Keresési előzmények</button>
    </a><br>

    <!-- Gomb új jármű hozzáadásához -->
    <br><a href="{{ route('vehicle.create') }}">
    <button>Új jármű hozzáadása</button>
    </a><br>

    <!-- Gomb a járművek szerkesztésehez -->
    <br><form action="{{ route('vehicle.edit') }}" method="GET">
        <label for="plate_number">Rendszám:</label>
        <input type="text" id="plate_number" name="plate_number" required>
        <br><button type="submit">Jármű szerkesztése</button>
    </form>

    <!-- Gomb új káresemény hozzáadásához -->
    <br><a href="{{ route('damage_event.createIncidents') }}">
    <button>Új káresemény hozzáadása</button>
    </a><br>

    <!-- Gomb a káresemény szerkesztésehez -->
    <br><form action="{{ route('damage_event.editIncidents') }}" method="GET">
        <label for="id">Káresemény ID-ja:</label>
        <input type="text" id="id" name="id" required>
        <br><button type="submit">káresemény szerkesztése</button>
    </form>

    <!-- Gomb a káresemény törlésére -->
    <br><form action="{{ route('damage_event.deleteIncidents') }}" method="GET">
        <label for="id">Káresemény ID-ja:</label>
        <input type="text" id="id" name="id" required>
        <br><button type="submit">káresemény törlése</button>
    </form>

    <!-- Gomb a prémium felhasználók kezelére -->
    <br><form action="{{ route('admin.manage_premium_users') }}" method="GET">
        <button type="submit">Prémium felhasználók kezelése</button>
    </form>
</body>
</html>