<!-- premium_users.blade.php -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Prémium felhasználók kezelése</title>
</head>
<body>
    <h1>Prémium felhasználók kezelése!</h1>

    <!-- Vissza a főoldalra -->
    <a href="/">
        <button style="position: absolute; top: 10px; right: 10px;">Vissza a főoldalra</button>
    </a>

    <!-- Hibaüzenetek megjelenítése -->
    @if(session('error'))
        <p style="color: red;">{{ session('error') }}</p>
    @endif

    @if(session('success'))
        <div style="color: green" class="alert alert-success">
            {{ session('success') }}
        </div><br>
    @endif

    <!-- Listázás -->
    @foreach ($users as $user)
        {{ $user->name }}
        @if ($user->is_premium)
            <span style="color: green;">Prémium felhasználó</span>
        @else
            <span style="color: red;">Nem prémium felhasználó</span>
        @endif

        <form action="{{ route('admin.toggle_premium_status', ['id' => $user->id]) }}" method="POST">
            @csrf
            @method('PUT')

            <button type="submit">Prémium váltás</button>
        </form>
    @endforeach

    <!-- Lapozás -->
    {{ $users->links('vendor.pagination.simple-default') }}


</body>
</html>

