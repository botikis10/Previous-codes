<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Vehicle;
use Illuminate\Support\Facades\Auth;

use Illuminate\Support\Facades\File;

class AdminVehicleController extends Controller
{
    public function create()
    {
        if (!Auth::user()->is_premium) {
            return redirect('/')->with('error', 'Csak prémium felhasználók érhetik el ezt az oldalt.'); 
        }
        return view('create');
    }

    public function store(Request $request)
    {
        $request->validate([
            'plate_number' => 'required|regex:/^[A-Za-z]{3}[-]?[0-9]{3}$/',
            'brand' => 'required',
            'type' => 'required',
            'manufacture_year' => 'required|integer|min:1900|max:2021',
            'image' => 'required|image|mimes:jpeg,png,jpg,gif|max:2048',
        ]);

        $plateNumber = substr_replace(strtoupper(preg_replace('/[^A-Za-z0-9]/', '', $request->plate_number)), '-', 3, 0);

        //if plateNumber is already in db
        if (Vehicle::where('plate_number', $plateNumber)->exists()) {
            return redirect()->route('vehicle.create')->with('error', 'A rendszám már szerepel az adatbázisban!');
        }

        $imagePath = $request->file('image')->store('vehicle_images', 'public');

        Vehicle::create([
            'plate_number' => $plateNumber,
            'brand' => $request->brand,
            'type' => $request->type,
            'manufacture_year' => $request->manufacture_year,
            'image' => $imagePath,
        ]);

        return redirect()->route('vehicle.create')->with('success', 'Jármű sikeresen hozzáadva!');
    }

    public function edit(Request $request)
    {
        if (!Auth::user()->is_premium) {
            return redirect('/')->with('error', 'Csak prémium felhasználók érhetik el ezt az oldalt.'); 
        }

        // Jó formátomú e a rendszám
        if (!preg_match('/^[A-Za-z]{3}[-]?[0-9]{3}$/', $request->plate_number)) {
            return redirect('/')->with('error', 'Hibás formátumú rendszám!');
        }

        $plateNumber = substr_replace(strtoupper(preg_replace('/[^A-Za-z0-9]/', '', $request->plate_number)), '-', 3, 0);
        $vehicle = Vehicle::where('plate_number', $plateNumber)->first();

        if (!$vehicle) {
            return redirect('/')->with('error', 'Nincs ilyen rendszámú jármű az adatbázisban!');
        }

        return view('edit', compact('vehicle'));
    }

    public function update(Request $request, $id)
    {
        $request->validate([
            'brand' => 'required',
            'type' => 'required',
            'manufacture_year' => 'nullable|integer|min:1900|max:2021',
            'image' => 'nullable|image|mimes:jpeg,png,jpg,gif|max:2048',
        ]);

        $vehicle = Vehicle::findOrFail($id);

        $vehicle->brand = $request->brand;
        $vehicle->type = $request->type;
        $vehicle->manufacture_year = $request->manufacture_year;

        if ($request->hasFile('image')) {
            $oldImagePath = $vehicle->image;

            $imagePath = $request->file('image')->store('vehicle_images', 'public');
            $vehicle->image = $imagePath;

            // Töröld az előző képet a tárhelyről
            if ($oldImagePath && File::exists(public_path('storage/' . $oldImagePath))) {
                File::delete(public_path('storage/' . $oldImagePath));
            }
        }

        $vehicle->save();

        return redirect('/')->with('success', 'Jármű sikeresen frissítve!');
    }
}
