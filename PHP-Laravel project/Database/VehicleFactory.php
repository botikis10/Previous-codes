<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\User>
 */
class VehicleFactory extends Factory
{
    public function definition(): array
    {
        return [
            //'plate_number' => strtoupper($this->faker->bothify('???###')), // Generál egy AAA123 formátumú rendszámot
            'plate_number' => substr_replace(strtoupper($this->faker->bothify('???###')), '-', 3, 0),
            'brand' => $this->faker->word,
            'type' => $this->faker->word,
            'manufacture_year' => $this->faker->numberBetween(1990, 2023),
            'image' => $this->faker->imageUrl(), // Vagy a tényleges kép feltöltése a szerverre
        ];
    }
}
