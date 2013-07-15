class Article < ActiveRecord::Base
  attr_accessible :title, :url

  belongs_to :entity
end
