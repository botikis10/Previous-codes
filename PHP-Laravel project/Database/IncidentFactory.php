<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use App\Models\Vehicle;
use App\Models\Incident;

class IncidentFactory extends Factory
{
    public function definition(): array
    {
        return [
            'location' => $this->faker->address,
            'date_time' => $this->faker->dateTimeThisYear(),
            'description' => $this->faker->text,
        ];
    }

    // Define a method to associate incidents with vehicles
    public function configure()
    {
        return $this->afterCreating(function (Incident $incident) {
            // Get random vehicle IDs from the vehicles table
            $vehicles = Vehicle::inRandomOrder()->limit(rand(1, 3))->get();

            // Attach the vehicles to the incident
            $incident->vehicles()->attach($vehicles);
        });
    }
}
