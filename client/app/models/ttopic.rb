class Ttopic < ActiveRecord::Base
  attr_accessible :name, :url

  has_and_belongs_to_many :sections
  has_many :clusters
  has_many :entities, through: :clusters
  has_many :articles, through: :entities

  validates :name, presence: true, uniqueness: true
  validates :url, presence: true, uniqueness: true
end
