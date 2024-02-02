package model

type Guild struct {
	ID     string `json:"id,omitempty" bson:"id,omitempty"`
	Name   string `json:"name"`
	Prefix string `json:"prefix"`
}
