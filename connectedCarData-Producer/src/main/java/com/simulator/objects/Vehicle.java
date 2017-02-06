package com.simulator.objects;

import java.io.Serializable;
import java.util.Map;



public class Vehicle implements Serializable{
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private String vin;
	private String make;
    private String model;
    private String year = "2016";
	private String type;
	
	
    public String getVin() {
		return vin;
	}
	public void setVin(String string) {
		this.vin = string;
	}
	public String getType() {
		return type;
	}
	public void setType(String type) {
		this.type = type;
	}
	public String getMake() {
		return make;
	}
	public void setMake(String make) {
		this.make = make;
	}
	public String getModel() {
		return model;
	}
	public void setModel(String model) {
		this.model = model;
	}
	public String getYear() {
		return year;
	}
	public void setYear(String year) {
		this.year = year;
	}
	

}
