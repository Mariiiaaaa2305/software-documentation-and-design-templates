using MyLab.Domain;

namespace MyLab.DataAccessLayer;

public interface IUserRepository
{
    // Отримати всіх користувачів із CSV файлу
    List<User> ReadUsersFromCsv(string filePath);
    
    // Зберегти список користувачів у базу даних
    void SaveUsersToDatabase(List<User> users);
}