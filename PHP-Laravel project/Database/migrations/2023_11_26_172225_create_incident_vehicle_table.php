<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('incident_vehicle', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('incident_id');
            $table->unsignedBigInteger('vehicle_id');
            $table->timestamps();
        
            $table->foreign('incident_id')->references('id')->on('incidents')->onDelete('cascade');
            $table->foreign('vehicle_id')->references('id')->on('vehicles')->onDelete('cascade');
        });        
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('incident_vehicle');
    }
};
