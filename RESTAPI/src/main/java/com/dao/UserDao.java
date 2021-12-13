package com.dao;

import java.util.List;

import org.hibernate.Query;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;

import com.db.HibernateTemplate;

import com.dto.User;

public class UserDao {
	public void register(User u) {
		Configuration config = new Configuration();
		config.configure("hibernate.cfg.xml");
		SessionFactory factory = config.buildSessionFactory();
		Session session = factory.openSession();
		session.save(u);
		Transaction tx = session.beginTransaction();
		tx.commit(); 
		session.close();
	}

	


	public User verifyLogin(String loginId) {
		Configuration config = new Configuration();
		config.configure("hibernate.cfg.xml");
		SessionFactory factory = config.buildSessionFactory();
		Session session = factory.openSession();	
		System.out.println(loginId);
		User user = (User) session.get(User.class, loginId);		
		return user;
	}
	




}
