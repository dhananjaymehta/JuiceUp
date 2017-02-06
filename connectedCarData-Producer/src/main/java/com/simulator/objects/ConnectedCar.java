package com.simulator.objects;

import java.io.Serializable;
import java.util.Date;

public class ConnectedCar extends Vehicle implements Serializable{

	/**
	 * 
	 */
	private static final long serialVersionUID = -363595938453721434L;
	
	private double latitude;
	private double longitude;
	private String fuel_type = "ELECTRIC";
	private int fuel_capacity;
	private Date eventTimestamp;

	public double getLatitude() {
		return latitude;
	}

	public double getLongitude() {
		return longitude;
	}

	public int getFuel_capacity() {
		return fuel_capacity;
	}

	public void setFuel_capacity(int fuel_capacity) {
		this.fuel_capacity = fuel_capacity;
	}

	public String getFuel_type() {
		return fuel_type;
	}

	public void setFuel_type(String fuel_type) {
		this.fuel_type = fuel_type;
	}

	public void setLatitude(double latitude) {
		this.latitude = latitude;
	}

	public void setLongitude(double longitude) {
		this.longitude = longitude;
	}

	public Date getEventTimestamp() {
		return eventTimestamp;
	}

	public void setEventTimestamp(Date eventTimestamp) {
		this.eventTimestamp = eventTimestamp;
	}
	
	@Override
	public String toString() {
		return getVin() + ", " + getLatitude() + "," + getLongitude() + "," + getFuel_capacity() + ","+ getEventTimestamp();
	}

}
