package main

import (
	"context"
	"fmt"
	"kokusei/api/model"
	"log"
	"time"

	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var (
	client *mongo.Client
)

func init() {
	MONGODB_URI := "mongodb://localhost:27017/"
	client_options := options.Client().ApplyURI(MONGODB_URI)
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	var err error
	client, err = mongo.Connect(ctx, client_options)
	if err != nil {
		log.Fatal(err)
	}

	err = client.Ping(ctx, nil)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Connected to MongoDB")
}

func main() {
	fmt.Print("haloo")
	app := fiber.New()

	DB_NAME := "kokusei"

	app.Get("/", func(c *fiber.Ctx) error {
		data := model.Guild{
			ID:     "1",
			Prefix: "!",
			Name:   "cloud",
		}
		return c.JSON(data)
	})

	app.Get("/guild", func(c *fiber.Ctx) error {
		collection := client.Database(DB_NAME).Collection("guild")
		cursor, err := collection.Find(context.Background(), bson.D{})
		if err != nil {
			return c.SendString(err.Error())
		}

		defer cursor.Close(context.Background())

		var guilds []model.Guild
		if err := cursor.All(context.Background(), &guilds); err != nil {
			return c.SendString("error modeling slice")
		}

		return c.JSON(guilds)
	})

	app.Post("/guild", func(c *fiber.Ctx) error {
		collection := client.Database(DB_NAME).Collection("guild")

		var new_guild model.Guild
		if err := c.BodyParser(&new_guild); err != nil {
			return c.SendString("Format is not supported")
		}

		result, err := collection.InsertOne(context.Background(), new_guild)
		if err != nil {
			return c.SendString("Failed to insert to DB")
		}

		return c.JSON(result.InsertedID)
	})

	app.Get("/guild/:id", func(c *fiber.Ctx) error {
		collection := client.Database(DB_NAME).Collection("guild")

		id := c.Params("id")

		var guild model.Guild
		if err := collection.FindOne(context.Background(), bson.M{"id": id}).Decode(&guild); err != nil {
			return c.SendString("Failed to return")
		}

		return c.JSON(guild)
	})

	app.Put("/guild/:id", func(c *fiber.Ctx) error {
		collection := client.Database(DB_NAME).Collection("guild")

		var updated_guild model.Guild
		if err := c.BodyParser(&updated_guild); err != nil {
			return c.SendString("Can't Parse")
		}

		id := c.Params("id")
		filter := bson.M{"_id": id}
		update := bson.M{"$set": updated_guild}
		_, err := collection.UpdateOne(context.Background(), filter, update)
		if err != nil {
			return c.SendString("Can't Update")
		}

		return c.SendString("Guild Updated")
	})

	app.Delete("/guild/:id", func(c *fiber.Ctx) error {
		collection := client.Database(DB_NAME).Collection("guild")
		id := c.Params("id")

		_, err := collection.DeleteOne(context.Background(), bson.M{"id": id})
		if err != nil {
			return c.SendString("Can't Delete")
		}

		return c.SendString("Guild Deleted")
	})

	app.Listen(":3000")
}
