class SectionsController < ApplicationController
  def show
    @sections = Section.all
    params[:id] = 1 if params[:id].nil?
    @section = Section.find(params[:id])
  end
end
