class Article < ActiveRecord::Base
  attr_accessible :title, :url

  #belongs_to :entity

  has_many :ref_entities

  validates :title, uniqueness: true
  validates :url, uniqueness: true
end
