from abc import ABC, abstractmethod

class UnitOfWork(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

class Repository(ABC):
    def __init__(self, connection):
        self.connection = connection

    def insert(self, query, value=None):
        cursor = self.connection.cursor()
        try:
            if value is None:
                cursor.execute(query)
            else:
                cursor.execute(query, value)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
        
    def update(self, query, value=None):
        cursor = self.connection.cursor()
        try:
            if value is None:
                cursor.execute(query)
            else:
                cursor.execute(query, value)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()         
        

    def delete(self, query, value=None):
        cursor = self.connection.cursor()
        try:
            if value is None:
                cursor.execute(query)
            else:
                cursor.execute(query, value)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()        
        

    def get(self, query, value=None):
        print(self.connection)
        cursor = self.connection.cursor()
        print(cursor)
        result = None
        try:
            if value is None:
                cursor.execute(query)
            else:
                cursor.execute(query, value)
            result = cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
        return result

    def commit(self):
        self.connection.commit()
        pass
    def rollback(self):
        self.connection.rollback()
        pass    
























    # @abstractmethod
    # def insert(self, query, value):
    #     pass

    # @abstractmethod
    # def update(self, query, value):
    #     pass

    # @abstractmethod
    # def delete(self, query, value):
    #     pass

    # @abstractmethod
    # def get(self, query, value):
    #     pass

    # @abstractmethod
    # def commit(self):
    #     pass

    # @abstractmethod
    # def rollback(self):
    #     pass

