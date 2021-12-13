package com.rest;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.sql.Date;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.Random;
import java.util.Set;

import javax.mail.Authenticator;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import javax.ws.rs.Consumes;
import javax.ws.rs.DELETE;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

import org.glassfish.jersey.media.multipart.FormDataContentDisposition;
import org.glassfish.jersey.media.multipart.FormDataParam;

import com.dao.*;
import com.dto.*;

@Path("myresource")
public class MyResource {
	@Path("hello")
	@GET
	@Produces(MediaType.TEXT_PLAIN)
	public String getIt() {
		return "Got it!";
	}



	@Path("registerUser")
	@POST
	@Consumes(MediaType.APPLICATION_JSON)
	public void registerUser(User u){
		String text=u.getPassword();
		String enc="";
		for(int i=0;i<text.length();i++){
			enc+=((int)text.charAt(i))+""+(char)(97+i);
		}
		u.setPassword(enc);
		UserDao daoH=new UserDao();
		daoH.register(u);
	}



	@Path("verifyLogin/{loginId}")
	@GET
	@Produces(MediaType.APPLICATION_JSON)
	public User verifyLogin(@PathParam("name") String name){
		System.out.println(name);
		UserDao daoH=new UserDao();
		User user=daoH.verifyLogin(name);
		String dec="";
		for(String str:user.getPassword().split("[a-zA-Z]+")){
			if(str.length()>0)
				dec+=(char)Integer.parseInt(str);
		}
		user.setPassword(dec);
		return user;
	}
}

