package com.dto;

import java.util.ArrayList;
import java.util.List;

import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import javax.persistence.OneToOne;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@XmlRootElement
public class User {
	@Id
	private String name;
	private String email;
	private String mno;
	private String dob;
	private String password;

	public User() {
		super();
	}
	public User(String name, String email, String mno, String dob, String password) {
		super();
		this.name = name;
		this.email = email;
		this.name = mno;
		this.name = dob;
		this.password = password;
	}
	
	public User(String name) {
		super();
		this.name = name;
	}
	
	public String getMno() {
		return mno;
	}
	public void setMno(String mno) {
		this.mno = mno;
	}
	public String getDob() {
		return dob;
	}
	public void setDob(String dob) {
		this.dob = dob;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getName() {
		return name;
	}
	public void setLoginId(String name) {
		this.name = name;
	}

	public String getEmail() {
		return email;
	}
	public void setEmail(String email) {
		this.email = email;
	}
	public String getPassword() {
		return password;
	}
	public void setPassword(String password) {
		this.password = password;
	}
	@Override
	public String toString() {
		return "User [name=" + name + ", email=" + email + ", mno = " + mno + ", dob = " + dob + ", password=" + password + "]";
	}
}
