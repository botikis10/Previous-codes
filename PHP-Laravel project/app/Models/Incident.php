<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Incident extends Model
{
    use HasFactory;

    protected $fillable = [
        'location',
        'date_time',
        'description',
    ];

    // kapcsolatok 
    public function vehicles()
    {
        return $this->belongsToMany(Vehicle::class);
    }
}
