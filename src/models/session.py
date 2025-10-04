from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from src.database.database import Base

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    parametros = Column(JSON, nullable=False) 
    csv_s3_key = Column(String, nullable=False) 
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationship with user
    user = relationship("User", back_populates="sessions")
    
    def __repr__(self):
        return f"<Session(id={self.id}, user_id={self.user_id})>"
    
    def get_s3_url(self, bucket_name: str, region: str = 'us-east-2'):
        # Retorna la URL pública de S3
        if not self.csv_s3_key:
            return None
        return f"https://{bucket_name}.s3.{region}.amazonaws.com/{self.csv_s3_key}"
