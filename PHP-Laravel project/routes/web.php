<?php

use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\SearchController;
use App\Http\Controllers\IncidentController;
use Illuminate\Support\Facades\Auth;
use App\Http\Controllers\SearchHistoryController;
use App\Http\Controllers\AdminVehicleController;
use App\Http\Controllers\AdminDamageEventController;
use App\Http\Controllers\AdminActionController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

//Route::get('/', [SearchController::class, 'showAllPlateNumbers']);

Route::get('/', function () {
    return view('home');
});


Route::post('/submit', [SearchController::class, 'search'])->name('submit.search');


Route::middleware('auth')->group(function () {
    Route::get('/incident/{id}', [IncidentController::class, 'show'])->name('incident_details');

    Route::get('/search-history', [SearchHistoryController::class, 'index'])->name('search_history');

    Route::get('/vehicles/create', [AdminVehicleController::class, 'create'])->name('vehicle.create');
    Route::post('/vehicles/store', [AdminVehicleController::class, 'store'])->name('vehicle.store');

    Route::get('/vehicles/edit', [AdminVehicleController::class, 'edit'])->name('vehicle.edit');
    Route::put('/vehicles/update/{id}', [AdminVehicleController::class, 'update'])->name('vehicle.update');

    Route::get('/damage-events/create', [AdminDamageEventController::class, 'create'])->name('damage_event.createIncidents');
    Route::post('/damage-events/store', [AdminDamageEventController::class, 'store'])->name('damage_event.store');

    Route::get('/damage-events//edit', [AdminDamageEventController::class, 'edit'])->name('damage_event.editIncidents');
    Route::put('/damage-events/update/{id}', [AdminDamageEventController::class, 'update'])->name('damage_event.update'); 
    Route::get('/damage-events//delete', [AdminDamageEventController::class, 'delete'])->name('damage_event.deleteIncidents');

    Route::get('/manage-premium-users', [AdminActionController::class, 'managePremiumUsers'])->name('admin.manage_premium_users');
    Route::put('/toggle-premium-status/{id}', [AdminActionController::class, 'togglePremiumStatus'])->name('admin.toggle_premium_status');

    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
});


require __DIR__.'/auth.php';
