<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use App\Models\User;

class AdminActionController extends Controller
{
    public function managePremiumUsers(Request $request)
    {
        if (!Auth::user()->is_premium) {
            return redirect('/')->with('error', 'Csak prémium felhasználók érhetik el ezt az oldalt.'); 
        }

        $users = User::paginate(10);

        return view('premium_users', compact('users'));
    }

    public function togglePremiumStatus(Request $request, $userId)
    {
        $user = User::findOrFail($userId);

        // Prémium státusz megváltoztatása

        // Ha a felhasználó prémium, akkor a prémium státuszát hamisra állítjuk, de a felhasználó admin, és ha a felhasználó admin
        // akkor prémiumnak is kéne lennie, így az admin jogot is elkéne venni, de nem teszem, mert nincs specifikálva ez a feladatban
        
        $user->is_premium = !$user->is_premium;
        $user->save();

        return redirect('/')->with('success', 'Prémium státusz sikeresen frissítve.');
    }
}
