class Article < ActiveRecord::Base
  attr_accessible :title, :url

  has_and_belongs_to_many :entities

  validates :title, uniqueness: true
  validates :url, uniqueness: true
end
