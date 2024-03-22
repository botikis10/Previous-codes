<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Vehicle;
use App\Models\SearchHistory;
use Illuminate\Support\Facades\Auth;

class SearchController extends Controller
{
    public function search(Request $request)
    {
        $plateNumber = $request->input('plate_number');

        // Ellenőrizni a bejelentkezést
        if (!auth()->check()) {
            // Átirányítás a bejelentkezési oldalra, ha nincs bejelentkezve
            return Redirect()->route('register')->with('error', 'A kereséshez jelentkezz be.');
                
            //->with('url.intended', route('submit.search', ['plate_number' => $plateNumber]));
        }

        $plateNumber = strtoupper($request->input('plate_number'));

        // Rendszám formátum ellenőrzése
        if (!preg_match('/^[A-Z]{3}-?\d{3}$/', $plateNumber)) {
            return redirect()->back()->with('error', 'Hibás rendszám formátum. Kérlek, adj meg helyes rendszámot! Rendszám: ' . $plateNumber);
        }

        // Ha a rendszámban nincs kötőjel, akkor beillesztünk egyet
        if (strpos($plateNumber, '-') === false) {
            $plateNumber = substr($plateNumber, 0, 3) . '-' . substr($plateNumber, 3);
        }

        // Keresés a jármű adatbázisban a rendszám alapján
        $vehicle = Vehicle::where('plate_number', $plateNumber)->first();

        if (!$vehicle) {
            return redirect()->back()->with('error', 'Nincs ilyen rendszámú jármű az adatbázisban. Rendszám: ' . $plateNumber);
        }

        // Káresemények lekérése az adott járműhöz időrendi sorrendben
        $incidents = $vehicle->incidents()->orderBy('date_time', 'desc')->get();

        // Keresési előzmény mentése
        $searchHistory = new SearchHistory();
        $searchHistory->user_id = Auth::id();
        $searchHistory->searched_plate_number = $plateNumber; 
        $searchHistory->search_time = now(); 
        $searchHistory->save();

        return view('results', compact('vehicle', 'incidents'));
    }

    public function showAllPlateNumbers()
    {
        $allVehicles = Vehicle::all();

        return view('all_plate_numbers', compact('allVehicles'));
    }
}
