from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Pet(BaseModel):
    id_pet: int
    name: str
    owner: str
    age: int

    def age_percentage(self, max_age: int = 20) -> float:
        """Calcula el porcentaje de edad en base a una expectativa de vida."""
        return (self.age / max_age) * 100


pets: List[Pet] = []


@app.post("/pets/", response_model=Pet)
def create_pet(pet: Pet):
    for existing_pet in pets:
        if existing_pet.id_pet == pet.id_pet:
            raise HTTPException(status_code=400, detail="ID already exists")
    pets.append(pet)
    return pet


@app.get("/pets/", response_model=List[Pet])
def get_pets():
    return pets


@app.get("/pets/{id_pet}", response_model=Pet)
def get_pet(id_pet: int):
    for pet in pets:
        if pet.id_pet == id_pet:
            return pet
    raise HTTPException(status_code=404, detail="Pet not found")


@app.put("/pets/{id_pet}", response_model=Pet)
def update_pet(id_pet: int, updated_pet: Pet):
    for i, pet in enumerate(pets):
        if pet.id_pet == id_pet:
            pets[i] = updated_pet
            return updated_pet
    raise HTTPException(status_code=404, detail="Pet not found")


@app.delete("/pets/{id_pet}")
def delete_pet(id_pet: int):
    for i, pet in enumerate(pets):
        if pet.id_pet == id_pet:
            del pets[i]
            return {"message": "Pet deleted successfully"}
    raise HTTPException(status_code=404, detail="Pet not found")


@app.get("/pets/{id_pet}/age_percentage")
def get_age_percentage(id_pet: int, max_age: int = 20):
    for pet in pets:
        if pet.id_pet == id_pet:
            return {"id_pet": id_pet, "age_percentage": pet.age_percentage(max_age)}
    raise HTTPException(status_code=404, detail="Pet not found")

