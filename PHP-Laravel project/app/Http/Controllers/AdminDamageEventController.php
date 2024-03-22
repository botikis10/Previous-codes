<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Vehicle;
use App\Models\Incident;
use Illuminate\Support\Facades\Auth;

class AdminDamageEventController extends Controller
{
    public function create()
    {
        if (!Auth::user()->is_premium) {
            return redirect('/')->with('error', 'Csak prémium felhasználók érhetik el ezt az oldalt.'); 
        }
        $vehicles = Vehicle::all();
        return view('createIncidents', compact('vehicles'));
    }

    public function store(Request $request)
    {
        $request->validate([
            'location' => 'required',
            'date_time' => 'required|date_format:Y-m-d\TH:i|before_or_equal:today',
            'vehicles' => 'required|array|min:1',
            'vehicles.*' => 'distinct',
        ]);

        $damageEvent = new Incident();
        $damageEvent->location = $request->location;
        $damageEvent->date_time = str_replace('T', ' ', $request->date_time) . ':00';;
        $damageEvent->description = $request->description ?? null;
        $damageEvent->save();

        $damageEvent->vehicles()->attach($request->vehicles);

        return redirect('/')->with('success', 'Új káresemény sikeresen létrehozva!');
    }

    public function edit(Request $request)
    {
        if (!Auth::user()->is_premium) {
            return redirect('/')->with('error', 'Csak prémium felhasználók szerkeszthetnek káreseményt.'); 
        }
        /*$damageEvent = Incident::findOrFail($request->id);
        if (!$damageEvent) {
            return redirect('/')->with('error', 'Nem létező káresemény!');
        }

        $vehicles = Vehicle::all();
        return view('editIncidents', compact('damageEvent', 'vehicles'));*/

        try {
            $damageEvent = Incident::findOrFail($request->id);
            $vehicles = Vehicle::all();
            return view('editIncidents', compact('damageEvent', 'vehicles'));
        } catch (\Illuminate\Database\Eloquent\ModelNotFoundException $e) {
            return redirect('/')->with('error', 'Nem létező káresemény!');
        }
    }

    public function update(Request $request, $id)
    {
        $request->validate([
            'location' => 'required',
            'date_time' => 'required|date_format:Y-m-d H:i:s|before_or_equal:today',
            'vehicles' => 'required|array|min:1',
            'vehicles.*' => 'distinct',
        ]);

        $damageEvent = Incident::findOrFail($id);
        $damageEvent->location = $request->location;
        $damageEvent->date_time = $request->date_time;
        $damageEvent->description = $request->description ?? null;
        $damageEvent->save();

        $damageEvent->vehicles()->sync($request->vehicles);

        return redirect('/')->with('success', 'Káresemény sikeresen frissítve!');
    }

    public function delete(Request $request)
    {
        if (!Auth::user()->is_premium) {
            return redirect('/')->with('error', 'Csak prémium felhasználók törölhetnek káreseményt.'); 
        }

        /*$damageEvent = Incident::findOrFail($request->id);
        if (!$damageEvent) {
            return redirect('/')->with('error', 'Nem létező káresemény!');
        }
        
        $damageEvent->delete();

        return redirect('/')->with('success', 'Káresemény sikeresen törölve!');*/

        try {
            $damageEvent = Incident::findOrFail($request->id);
            $damageEvent->delete();
    
            return redirect('/')->with('success', 'Káresemény sikeresen törölve!');
        } catch (\Illuminate\Database\Eloquent\ModelNotFoundException $e) {
            return redirect('/')->with('error', 'Nem létező káresemény!');
        }
    }
}
