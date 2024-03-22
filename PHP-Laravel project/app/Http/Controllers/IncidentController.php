<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Incident;
use App\Models\Vehicle;
use Illuminate\Support\Facades\Auth;

class IncidentController extends Controller
{
    //public function show($incident, $vehicle)
    public function show($id)
    {
        $incident = Incident::findOrFail($id);

        // Ellenőrizzük, hogy a felhasználó prémium-e
        if (!Auth::user()->is_premium) {
            return redirect('/')->with('error', 'Csak prémium felhasználók érhetik el ezt az oldalt.'); 
        }

        return view('incident_details', compact('incident'));
    }
}
