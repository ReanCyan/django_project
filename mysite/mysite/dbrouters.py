class BlogRouter:
	#  A router to control all database operations on the models in the blog application

	def db_for_read(self, model, **hints):
		# Attempts to read blog models go to blog_db
		if model._meta.app_label == 'blog':
			return 'blog_db'
		return None

	def db_for_write(self, model, **hints):
		# Attempts to write blog models go to blog_db
		if model._meta.app_label == 'blog':
			return 'blog_db'
		return None

	def allow_relation(self, obj1, obj2, **hints):
		# Allow relation only if a model in the blog is involved
		if obj1._meta.app_label == 'blog' or \
		   obj2._meta.app_label == 'blog':
			return True
		return None

	def allow_migrate(self, db, app_label, model_name=None, **hints):
		# Make sure the blog app only appears in the 'blog_db' database
		if app_label == 'blog':
			return db == 'blog_db'
		return None